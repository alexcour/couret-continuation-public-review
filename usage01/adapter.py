"""HTTP-only observation adapter. It never imports the target implementation."""
import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


class AdapterError(RuntimeError):
    pass


def label(observation):
    return json.dumps(observation, sort_keys=True, separators=(",", ":"))


class HttpAdapter:
    """The declared observation is (decision, view); preparation returns view.

    Each cache miss gets its own fresh session. Cache use requires a stationary,
    deterministic target with reliable independent preparation. Failures never
    become observations or a conformance certificate.
    """
    def __init__(self, config, journal):
        self.config = config
        self.base_url = config['base_url'].rstrip('/')
        self.alphabet = tuple(config['actions'])
        if not self.alphabet or len(set(self.alphabet)) != len(self.alphabet):
            raise AdapterError('Action alphabet must be nonempty and unique')
        if not isinstance(config['max_states'], int) or config['max_states'] < 1:
            raise AdapterError('A positive independent state bound is required')
        self.cache = {}
        self.stage = 'learning'
        self.stats = {}
        self.journal = Path(journal)
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        self.journal.write_text('', encoding='utf-8')

    def _counts(self):
        return self.stats.setdefault(self.stage, {
            'query_requests': 0, 'cache_hits': 0, 'preparations': 0,
            'event_calls': 0, 'failed_requests': 0, 'release_calls': 0})

    def post(self, path, body):
        headers = {'Content-Type': 'application/json'}
        token_name = self.config.get('token_env')
        if token_name:
            token = os.environ.get(token_name)
            if not token:
                raise AdapterError('Configured authentication environment variable is absent')
            headers['Authorization'] = 'Bearer ' + token
        request = Request(self.base_url + path, json.dumps(body).encode(), headers, method='POST')
        try:
            with urlopen(request, timeout=self.config.get('timeout_seconds', 10)) as response:
                result = json.load(response)
        except (URLError, OSError, ValueError) as exc:
            self._counts()['failed_requests'] += 1
            # Do not include response bodies or authentication values in diagnostics.
            raise AdapterError('HTTP request failed at ' + path) from exc
        if not isinstance(result, dict):
            raise AdapterError('Expected a JSON object at ' + path)
        return result

    def query(self, word, fresh=False):
        word = tuple(word)
        if any(action not in self.alphabet for action in word):
            raise AdapterError('Unknown action in query')
        counts = self._counts()
        counts['query_requests'] += 1
        if word in self.cache and not fresh:
            counts['cache_hits'] += 1
            return self.cache[word]
        prepared = self.post(self.config.get('prepare_path', '/prepare'), {})
        if 'session' not in prepared or 'view' not in prepared:
            raise AdapterError('Preparation must return session and view')
        counts['preparations'] += 1
        session = prepared['session']
        observations = []
        try:
            for action in word:
                raw = self.post(self.config.get('step_path', '/step'),
                                {'session': session, 'action': action})
                counts['event_calls'] += 1
                if not isinstance(raw.get('decision'), str) or not isinstance(raw.get('view'), str):
                    raise AdapterError('Step must return string decision and view')
                observations.append({'decision': raw['decision'], 'view': raw['view']})
        finally:
            # Releasing a prepared test instance is a separate operational cost.
            if self.config.get('release_path'):
                self.post(self.config['release_path'], {'session': session})
                counts['release_calls'] += 1
        record = {'word': list(word), 'initial_view': prepared['view'],
                  'observations': observations,
                  'final_view': observations[-1]['view'] if observations else prepared['view']}
        with self.journal.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'stage': self.stage, **record}, ensure_ascii=False) + '\n')
        previous = self.cache.get(word)
        if previous is not None and previous != record:
            raise AdapterError('Repeated preparation/query changed its observation: target is not stationary deterministic')
        self.cache[word] = record
        return record

    def membership(self, word):
        return tuple(label(item) for item in self.query(word)['observations'])

    def totals(self):
        keys = next(iter(self.stats.values())).keys() if self.stats else ()
        counts = {key: sum(row[key] for row in self.stats.values()) for key in keys}
        counts['successful_http_calls'] = (counts.get('preparations', 0) +
                                          counts.get('event_calls', 0) + counts['release_calls'])
        return counts
