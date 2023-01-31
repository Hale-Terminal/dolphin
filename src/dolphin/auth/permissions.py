import logging
from abc import ABC, abstractmethod

from fastapi import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from dolphin.enums import UserRoles
from dolphin.auth.service import get_current_user


log = logging.getLogger(__name__)


def any_permission(permissions: list, request: Request) -> bool:
    for p in permissions:
        try:
            p(request=request)
            return True
        except HTTPException:
            pass
    return False


class BasePermission(ABC):
    error_msg = [{"msg": "You don't have permission to access or modify this resource."}]
    status_code = HTTP_403_FORBIDDEN
    role = None

    @abstractmethod
    def has_required_permissions(self, request: Request) -> bool:
        ...

    def __init__(self, request: Request):
        user = get_current_user(request=request)
        if not user:
            raise HTTPException(status_code=self.status_code, detail=self.error_msg)

        self.role = user.role

        if not self.has_required_permissions(request=request):
            raise HTTPException(status_code=self.status_code, detail=self.error_msg)


class PermissionDependency(object):
    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    def __call__(self, request: Request):
        for permission_class in self.permissions_classes:
            permission_class(request=request)


class AdminPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        return self.role == UserRoles.admin


class ManagerPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        permission = any_permission(
            permissions=[
                AdminPermission,
            ],
            request=request,
        )
        if not permission:
            if self.role == UserRoles.manager:
                return True
        return permission


class MemberPermission(BasePermission):
    def has_required_permissions(self, request: Request) -> bool:
        permission = any_permission(
            permissions=[
                AdminPermission,
                ManagerPermission,
            ],
            request=request,
        )
        if not permission:
            if self.role == UserRoles.member:
                return True
        return permission
