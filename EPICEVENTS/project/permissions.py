from rest_framework import permissions


class IsSalesContact(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if view.action in ['list', "retrieve"]:
            return True
        elif view.action == 'create':
            return request.user.team == 'SALE'
        return obj.sales_contact == request.user


class IsSupportContactOrSalesContact(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.support_contact == request.user or obj.client.sales_contact == request.user
