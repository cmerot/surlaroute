import hashlib
import uuid

from app.core.db.models import (
    Activity,
    AssociationOrgActor,
    Org,
    Person,
)


def get_fixture_uuid(seed: str) -> uuid.UUID:
    # Create a namespace UUID (this can be any UUID, but it's common to use a well-known one)
    namespace_uuid = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

    # Create a hash object using the seed
    hash_object = hashlib.sha1(seed.encode("utf-8")).hexdigest()

    # Generate the UUID using the namespace and the hash object
    deterministic_uuid = uuid.uuid5(namespace_uuid, hash_object)

    return deterministic_uuid


activity_fixtures = [
    Activity(name="cat", path="cat"),
    Activity(name="big", path="cat.big"),
    Activity(name="lion", path="cat.big.lion"),
    Activity(name="tiger", path="cat.big.tiger"),
    Activity(name="jaguar", path="cat.big.jaguar"),
    Activity(name="small", path="cat.small"),
    Activity(name="wild", path="cat.small.wild"),
    Activity(name="ocelot", path="cat.small.wild.ocelot"),
    Activity(name="bobcat", path="cat.small.wild.bobcat"),
    Activity(name="domestic", path="cat.small.domestic"),
    Activity(name="persian", path="cat.small.domestic.persian"),
    Activity(name="bengal", path="cat.small.domestic.bengal"),
    Activity(name="shorthair", path="cat.small.domestic.shorthair"),
]

robert = Person(firstname="Robert", lastname="Mitchum", id=get_fixture_uuid("robert"))
eddie = Person(firstname="Eddie", lastname="Coyle", id=get_fixture_uuid("eddie"))
person_fixtures = [robert, eddie]

armodo = Org(name="armodo", id=get_fixture_uuid("armodo"))
slowfest = Org(name="slowfest", id=get_fixture_uuid("slowfest"))
org_fixtures = [armodo, slowfest]

om1 = AssociationOrgActor(org=armodo, actor=robert)
om2 = AssociationOrgActor(org=armodo, actor=slowfest)
om3 = AssociationOrgActor(org=slowfest, actor=eddie)
om_fixtures = [om1, om2, om3]
