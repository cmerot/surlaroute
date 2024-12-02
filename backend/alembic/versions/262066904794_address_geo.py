"""address_geo

Revision ID: 262066904794
Revises: 049cd2cd269f
Create Date: 2024-12-02 17:39:44.280899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = '262066904794'
down_revision: Union[str, None] = '049cd2cd269f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addressgeo', sa.Column('geom_point', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True))
    op.add_column('addressgeo', sa.Column('geom_shape', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True))
    op.drop_index('idx_addressgeo_geo_location', table_name='addressgeo', postgresql_using='gist')
    op.drop_index('idx_addressgeo_geo_shape', table_name='addressgeo', postgresql_using='gist')
    # op.create_index('idx_addressgeo_geom_point', 'addressgeo', ['geom_point'], unique=False, postgresql_using='gist')
    # op.create_index('idx_addressgeo_geom_shape', 'addressgeo', ['geom_shape'], unique=False, postgresql_using='gist')
    op.drop_column('addressgeo', 'geo_location')
    op.drop_column('addressgeo', 'geo_shape')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addressgeo', sa.Column('geo_shape', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', _spatial_index_reflected=True), autoincrement=False, nullable=True))
    op.add_column('addressgeo', sa.Column('geo_location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', _spatial_index_reflected=True), autoincrement=False, nullable=True))
    op.drop_index('idx_addressgeo_geom_shape', table_name='addressgeo', postgresql_using='gist')
    op.drop_index('idx_addressgeo_geom_point', table_name='addressgeo', postgresql_using='gist')
    op.create_index('idx_addressgeo_geo_shape', 'addressgeo', ['geo_shape'], unique=False, postgresql_using='gist')
    op.create_index('idx_addressgeo_geo_location', 'addressgeo', ['geo_location'], unique=False, postgresql_using='gist')
    op.drop_column('addressgeo', 'geom_shape')
    op.drop_column('addressgeo', 'geom_point')
    # ### end Alembic commands ###
