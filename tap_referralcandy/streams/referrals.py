import singer
import json
import time
from datetime import datetime
from referral_candy import ReferralCandy
from singer import metadata

LOGGER = singer.get_logger()

class Referrals:
    def __init__(self):
        self._start_date = ""
        self._state = {}

    @property
    def name(self):
        return "referrals"

    @property
    def key_properties(self):
        return ["shopify_order_number"]

    @property
    def replication_key(self):
        return "referral_timestamp"

    @property
    def replication_method(self):
        return "INCREMENTAL"

    @property
    def state(self):
        return self._state
    
    def get_metadata(self, schema):
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=self.key_properties,
            valid_replication_keys=[self.replication_key],
            replication_method=self.replication_method,
        )
        return mdata
    
    def get_tap_data(self, config, state):
        access_id = config["access_id"]
        secret_key = config["secret_key"]

        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        self._start_date = round(datetime.timestamp(datetime.strptime(config.get("start_date", today), "%Y-%m-%dT%H:%M:%S")))
        self._state = state.copy()

        state_date = self._state.get('referrals', self._start_date)
        period_from = max(self._start_date, state_date)
        max_rep_key = period_from

        resp = ReferralCandy(access_id=access_id, secret_key=secret_key).referrals({'period_from': period_from})
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            for referral_record in resp['referrals']:
                rep_key = referral_record.get(self.replication_key)
                if rep_key and rep_key > max_rep_key:
                    max_rep_key = rep_key
                yield self.data_processing(referral_record)

        self._state['referrals'] = max_rep_key  

    def data_processing(self, referral_record):
        referral_record["shopify_order_number"] = int(referral_record["external_reference_id"])
        referral_record.pop("external_reference_id", None)
        referral_record["referral_order_time"]  = datetime.fromtimestamp(referral_record["referral_timestamp"]).isoformat() 
        return referral_record
