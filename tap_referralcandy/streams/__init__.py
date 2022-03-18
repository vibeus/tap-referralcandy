from .referrals import Referrals

def create_stream(stream_id):
    if stream_id == "referrals":
        return Referrals()

    assert False, f"Unsupported stream: {stream_id}"
