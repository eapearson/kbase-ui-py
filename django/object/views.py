from lib.ServiceUtils import ServiceUtils
from django.shortcuts import render
from lib.GenericClient import GenericClient
from django.conf import settings

def get_object_info(token, object_identity):
    workspace_url = settings.KBASE['services']['workspace']['url']
    client = GenericClient(module='Workspace', url=workspace_url, token=token, timeout=60)
    object_info = client.call_func('get_object_info3', {
        'objects': [object_identity]
    })['infos'][0]

    return ServiceUtils.obj_info_to_object(object_info)

def get_workspace_info(token, workspace_identity):
    workspace_url = settings.KBASE['services']['workspace']['url']
    client = GenericClient(module='Workspace', url=workspace_url, token=token, timeout=60)
    workspace_info = client.call_func('get_workspace_info', workspace_identity)

    return ServiceUtils.ws_info_to_object(workspace_info)

def build_identity(workspace, object, object_version):
    object_identity = {}
    workspace_identity = {}
    if workspace.isnumeric():
        object_identity['wsid'] = int(workspace)
        workspace_identity['id'] = int(workspace)
    else:
        object_identity['workspace'] = workspace
        workspace_identity['workspace'] = workspace
    
    if object.isnumeric():
        object_identity['objid'] = int(object)
    else:
        object_identity['name'] = object

    if object_version is not None:
        object_identity['ver'] = object_version

    return workspace_identity, object_identity

def index(request, workspace, object, object_version=None):
    token = request.kbase['auth']['token']
    workspace_identity, object_identity = build_identity(workspace, object, object_version)

    # Get object info
    try:
        object_info = get_object_info(token, object_identity)
        workspace_info = get_workspace_info(token, workspace_identity)
        print(object_info)
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
            "object/index.html",
            {"page": {"title": "Object Landing Page"}, 
            "workspace": workspace,
            "object": object,
            "object_version": object_version,
            "object_info": object_info,
            'workspace_info': workspace_info,
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": "index"
            }
        )

    # Error if inadequate permissin

    # Is the type in our supported types dict?

    # If so, dispatch to the associated view.

    # Otherwise, show default view.
    
def overview(request, workspace, object, object_version=None):
    token = request.kbase['auth']['token']
    workspace_identity, object_identity = build_identity(workspace, object, object_version)

    # Get object info
    try:
        object_info = get_object_info(token, object_identity)
        workspace_info = get_workspace_info(token, workspace_identity)
        print(object_info)
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
            "object/overview.html",
            {"page": {"title": "Object Landing Page"}, 
            "workspace": workspace,
            "object": object,
            "object_version": object_version,
            "object_info": object_info,
            'workspace_info': workspace_info,
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": "overview"
            }
        )

   
def provenance(request, workspace, object, object_version=None):
    token = request.kbase['auth']['token']
    workspace_identity, object_identity = build_identity(workspace, object, object_version)

    # Get object info
    try:
        object_info = get_object_info(token, object_identity)
        workspace_info = get_workspace_info(token, workspace_identity)
        print(object_info)
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
            "object/provenance.html",
            {"page": {"title": "Object Landing Page - Provenance"}, 
            "workspace": workspace,
            "object": object,
            "object_version": object_version,
            "object_info": object_info,
            'workspace_info': workspace_info,
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": "provenance"
            }
        )


   
def related_data(request, workspace, object, object_version=None):
    token = request.kbase['auth']['token']
    workspace_identity, object_identity = build_identity(workspace, object, object_version)

    # Get object info
    try:
        object_info = get_object_info(token, object_identity)
        workspace_info = get_workspace_info(token, workspace_identity)
        print(object_info)
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
            "object/related-data.html",
            {"page": {"title": "Object Landing Page - Related Data"}, 
            "workspace": workspace,
            "object": object,
            "object_version": object_version,
            "object_info": object_info,
            'workspace_info': workspace_info,
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": "related-data"
            }
        )


   
def linked_samples(request, workspace, object, object_version=None):
    token = request.kbase['auth']['token']
    workspace_identity, object_identity = build_identity(workspace, object, object_version)

    # Get object info
    try:
        object_info = get_object_info(token, object_identity)
        workspace_info = get_workspace_info(token, workspace_identity)
        print(object_info)
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
            "object/linked-samples.html",
            {"page": {"title": "Object Landing Page - Linked Samples"}, 
            "workspace": workspace,
            "object": object,
            "object_version": object_version,
            "object_info": object_info,
            'workspace_info': workspace_info,
            'settings': settings.KBASE,
            "kbase": request.kbase,
            "tab": "linked-samples"
            }
        )