"""
Queue api functions as a mixin
"""

import yaml
import json
from json import dumps, loads
from time import time
from base64 import b64decode
from jaseci.svc import CommonService
from jaseci.svc.common import Kube, UNSAFE_PARAPHRASE
from jaseci.api.interface import Interface


class JsOrcApi:
    """
    API for managing JsOrc
    """

    @Interface.admin_api()
    def load_yaml(self, files: list, namespace: str = "default"):
        """
        applying list of yaml files without associating to any modules/services
        """

        if self._h.meta.is_automated():
            kube = self._h.meta.app.kubernetes
            kube: Kube

            res = {}

            for file in files:
                for conf in yaml.safe_load_all(b64decode(file["base64"])):
                    kind = conf["kind"]
                    kube.create(kind, namespace, conf)
                    if not res.get(kind):
                        res[kind] = []
                    res[kind].append(conf)

            return res
        else:
            return {"message": "load_yaml is not supported on non automated JsOrc!"}

    @Interface.admin_api(cli_args=["name"])
    def apply_yaml(self, name: str, file: list, unsafe_paraphrase: str = ""):
        """
        apply manifest yaml to specific service
        """

        new_config = {}

        config_version = str(time())

        for conf in yaml.safe_load_all(b64decode(file[0]["base64"])):
            kind = conf["kind"]
            labels = conf.get("metadata").get("labels")
            if not labels.get("config_version"):
                labels["config_version"] = config_version

            if not new_config.get(kind):
                new_config[kind] = []
            new_config[kind].append(conf)

        old_config = self._h.get_glob(name)
        if old_config:
            old_config = loads(old_config)
            old_config.pop("__OLD_CONFIG__", None)
            for kind, confs in old_config.items():
                names = []
                for conf in confs:
                    names.append(conf["metadata"]["name"])
                old_config[kind] = names

            new_config["__OLD_CONFIG__"] = old_config

            if unsafe_paraphrase == UNSAFE_PARAPHRASE:
                new_config["__UNSAFE_PARAPHRASE__"] = unsafe_paraphrase

        self._h.save_glob(name, dumps(new_config))

        return new_config

    @Interface.admin_api(cli_args=["name"])
    def service_refresh(self, name: str):
        """
        refreshing service's config. If JsOrc is not automated, service will restart else JsOrc will handle the rest
        """

        hook = self._h

        to_start = not hook.meta.is_automated()

        service = getattr(hook, name, None)

        response = {"success": False}

        if isinstance(service, CommonService):
            service.reset(hook, to_start)
            response["success"] = True
        else:
            response[
                "message"
            ] = f"{name} is not a valid service. Can not refresh config."

        return response

    @Interface.admin_api(cli_args=["name"])
    def service_call(self, svc: str, attrs: list = []):
        """
        temporary api for retreiving/calling attributes of specific instance.
        """

        from jaseci.svc import MetaService

        meta = self._h.meta
        meta: MetaService

        svc = meta.get_service(svc)

        if not svc:
            return "Service (svc) field is required!"

        if not attrs:
            return "Attributes (attrs) field is required!"

        res = svc
        for at in attrs:
            attr = at.get("attr", False)
            if attr:
                res = getattr(res, attr)

            if callable:
                args = at.get("args", [])
                kwargs = at.get("kwargs", {})
                res = res(*args, **kwargs)

        try:
            # test if json serializable
            json.dumps(res)
            return res
        except Exception:
            return {"error": f"Not JSON Serializable! class {res.__class__.__name__}"}
