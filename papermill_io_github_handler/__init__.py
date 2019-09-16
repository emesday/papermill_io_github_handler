import base64
import json
import os
import re
import urllib.parse

import requests


class GitHubHandler(object):

    last_data = None

    @classmethod
    def _parse(cls, path):
        url = urllib.parse.urlparse(path)
        try:
            user, repo, blob, ref, sub_path = re.match(
                r"^/(?P<user>[^/]+)/(?P<repo>[^/]+)/(?P<blob>[^/]+)/(?P<ref>[^/]+)/(?P<subpath>.*)",
                url.path).group('user', 'repo', 'blob', 'ref', 'subpath')
        except AttributeError:
            raise AttributeError("path must be github+https://<github_url>/<user>/<repo>/blob/<ref>/<sub_path>")
        endpoint = 'https://api.github.com'
        if url.netloc != 'github.com':
            endpoint = 'https://{}/api/v3'.format(url.netloc)
        api_url = '{endpoint}/repos/{user}/{repo}/contents/{sub_path}'.format(
            endpoint=endpoint, user=user, repo=repo, sub_path=sub_path)
        params = {'ref': ref, 'branch': ref}
        custom_token_key = url.netloc.replace('.', '_').upper() + '_API_TOKEN'
        token = os.environ.get("GITHUB_API_TOKEN", '')
        token = os.environ.get(custom_token_key, token)
        assert token != '', "GITHUB_API_TOKEN or {} must be in Environment for {}".format(custom_token_key, url.netloc)
        auth = ('', token)
        commit_message = os.environ.get("GIT_MESSAGE", 'updated by papermill')
        committer = {
            'name': os.environ.get("GIT_NAME", 'papermill'),
            'email': os.environ.get("GIT_EMAIL", '(none)')
        }
        return api_url, params, auth, committer, commit_message

    @classmethod
    def read(cls, path):
        api_url, params, auth, _, _ = cls._parse(path)
        result = requests.request('GET', api_url, params=params, auth=auth)
        result.raise_for_status()
        result = result.json()
        content = base64.b64decode(result['content']).decode('utf-8')
        return content

    @classmethod
    def listdir(cls, path):
        raise NotImplementedError('listdir is not supported by GitHubHandler')

    @classmethod
    def write(cls, buf, path):
        api_url, params, auth, committer, message = cls._parse(path)
        resp = requests.request('GET', api_url, params=params, auth=auth)
        sha = None
        if resp.status_code == 200:
            sha = resp.json()['sha']
        data = {
            'message': message,
            'committer': committer,
            'branch': params['ref'],
            'content': base64.b64encode(buf.encode('utf-8')).decode('utf-8')
        }
        if sha:
            data['sha'] = sha
        data = json.dumps(data)
        result = requests.request('PUT', api_url, data=data, auth=auth)
        result.raise_for_status()

    @classmethod
    def pretty_path(cls, path):
        return path


