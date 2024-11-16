Traceback (most recent call last):
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/google/api_core/grpc_helpers.py", line 76, in error_remapped_callable
    return callable_(*args, **kwargs)
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/grpc/_channel.py", line 1181, in __call__
    return _end_unary_response_blocking(state, call, False, None)
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/grpc/_channel.py", line 1006, in _end_unary_response_blocking
    raise _InactiveRpcError(state)  # pytype: disable=not-instantiable
grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
	status = StatusCode.UNAVAILABLE
	details = "DNS resolution failed for generativelanguage.googleapis.com:443: C-ares status is not ARES_SUCCESS qtype=SRV name=_grpclb._tcp.generativelanguage.googleapis.com: Could not contact DNS servers"
	debug_error_string = "UNKNOWN:Error received from peer  {created_time:"2024-10-11T00:36:25.962434-04:00", grpc_status:14, grpc_message:"DNS resolution failed for generativelanguage.googleapis.com:443: C-ares status is not ARES_SUCCESS qtype=SRV name=_grpclb._tcp.generativelanguage.googleapis.com: Could not contact DNS servers"}"
>
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/Users/majumdar.sh/PycharmProjects/MetaMosaic/MetaMosaic/Gemini_Scripts/gemini_pro.py", line 99, in <module>
    img = process_image(img_file_path,image_front)
  File "/Users/majumdar.sh/PycharmProjects/MetaMosaic/MetaMosaic/Gemini_Scripts/gemini_pro.py", line 22, in process_image
    return genai.upload_file(file_path)
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/google/generativeai/files.py", line 71, in upload_file
    response = client.create_file(
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/google/generativeai/client.py", line 116, in create_file
    return self.get_file({"name": result["file"]["name"]})
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/google/ai/generativelanguage_v1beta/services/file_service/client.py", line 923, in get_file
    response = rpc(
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/google/api_core/gapic_v1/method.py", line 131, in __call__
    return wrapped_func(*args, **kwargs)
  File "/Users/majumdar.sh/Library/Python/3.9/lib/python/site-packages/google/api_core/grpc_helpers.py", line 78, in error_remapped_callable
    raise exceptions.from_grpc_error(exc) from exc
google.api_core.exceptions.ServiceUnavailable: 503 DNS resolution failed for generativelanguage.googleapis.com:443: C-ares status is not ARES_SUCCESS qtype=SRV name=_grpclb._tcp.generativelanguage.googleapis.com: Could not contact DNS servers
