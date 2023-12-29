from rest_framework.permissions import BasePermission


class HasScope(BasePermission):
    def has_permission(self, request, view):
        scopes: str = request.auth.payload.get("scopes")
        scopes_list = scopes.split(sep=" ")
        method_scopes = view.required_scopes[request.method.lower()]
        return any(
                all(scope in scopes_list for scope in req_scopes)
                for req_scopes in method_scopes
        )


