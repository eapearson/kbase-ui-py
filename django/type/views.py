from django.shortcuts import render
from lib.GenericClient import GenericClient
from lib.ServiceUtils import ServiceUtils
from django.conf import settings
import re


def get_type_info(token, type_id):
    workspace_url = settings.KBASE['services']['workspace']['url']
    client = GenericClient(module='Workspace', url=workspace_url, token=token, timeout=60)
    type_info = client.call_func('get_type_info', type_id)

    return type_info

def get_module_info(token, module_name, version):
    workspace_url = settings.KBASE['services']['workspace']['url']
    client = GenericClient(module='Workspace', url=workspace_url, token=token, timeout=60)

    params = {
        'mod': module_name
    }
    if version is not None:
        params['ver'] = version

    module_info = client.call_func('get_module_info', params)

    module_versions = client.call_func('list_module_versions', {'mod': module_name})

    return module_info, module_versions

def index(request, type, tab=None):
    token = request.kbase['auth']['token']
    [type_module, type_name, type_major_version, type_minor_version] = re.split(r"-|\.", type)
    try:
        type_info = get_type_info(token, type)
        print(type_info.keys())
    except Exception as ex:
        print('error')
        print(str(ex))
        return render(request, "error/index.html", {
                "page": {"title": "Error"},
                "error": str(ex),
                "kbase": request.kbase,
                "request": request
            })
    else:
        return render(
            request,
            "type/index.html",
            {"page": {"title": f"{type_name} ({type_major_version}.{type_minor_version}) | Type Landing Page"}, 
            "type_info": type_info,
            "type": {
                "module": type_module,
                "name": type_name,
                "version": {
                    "major": type_major_version,
                    "minor": type_minor_version
                }
            },
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": tab or "home"
            }
        )

def module(request, module, version=None, tab=None):
    token = request.kbase['auth']['token']
    # [type_module, type_name, type_major_version, type_minor_version] = re.split(r"-|\.", type)
    try:
        module_info, module_versions = get_module_info(token, module, version)
        print(module_info, module_versions)
    except Exception as ex:
        print('error')
        print(str(ex))
        return render(request, "error/index.html", {
                "page": {"title": "Error"},
                "error": str(ex),
                "kbase": request.kbase,
                "request": request
            })
    else:
        return render(
            request,
            "type/module.html",
            {"page": {"title": f"{module} ({module_info['ver']}) | Module Landing Page"}, 
            "module_name": module,
            "module_info": module_info,
            "module_versions": module_versions,
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": tab or "home"
            }
        )
