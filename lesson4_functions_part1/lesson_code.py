import asyncio

is_requestor_global_admin, requested_relations, requested_user_info = await asyncio.gather(
    ory_client.has_admin_access(requestor.id),
    ory_client.get_relation_tuples(user_id),
    ...
)
if not is_global_admin:
    requestor_relations = await ory_client.get_relation_tuples(requestor.id)
    requestor_roles = RolesProcessor.process_requestor_roles(requestor_relations)
    roles = RolesProcessor.match_requested_and_requestor_roles(
        requestor_roles=requestor_roles,
        requested_roles=RolesProcessor.process_requested_roles(requested_relations)
    )
    if not requestor_roles.user_policy or requestor_roles.user_policy == PartnerAccessPolicy.EXTERNAL_USER:
        requestor_policy = "external_user"
        response_user_type = ExternalUser.from_user_info()
    else:
        response_requestor_policy = "internal_user"
        response_user_type = InternalUser.from_user_info()

else:
    roles = RolesProcessor.process_requested_roles(requested_relations)
    response_requestor_policy = "internal_user"
    response_user_type = InternalUser()