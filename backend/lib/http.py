from typing import Dict

from infrastructure.http import HTTPClient, HTTPClientMode

_http_clients: Dict[HTTPClientMode, HTTPClient] = {}

def get_http_client(mode: HTTPClientMode = HTTPClientMode.sync, headers: dict = None) -> HTTPClient:
	global _http_clients

	if headers is None:
		headers = {}

	if not isinstance(headers, dict):
		raise TypeError("headers must be a dictionary")

	if mode not in _http_clients:
		client = HTTPClient(mode=mode, headers=headers)

		if mode == HTTPClientMode.sync:
			client.get_client()
		else:
			client.get_async_client()

		_http_clients[mode] = client

	return _http_clients[mode]
