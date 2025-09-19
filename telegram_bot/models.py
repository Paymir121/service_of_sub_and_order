from sqlalchemy import  MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import DeclarativeBase, registry
import logging

from db import Connection

import logging

class Base(DeclarativeBase):
    md = MetaData()
    metadata = md
    metadata.reflect(
        bind=Connection().engine,
        views=True,
        extend_existing=True,
    )
    registry = registry(
        metadata=metadata
    )

def get_automapped():
    conn = Connection()
    automapped = automap_base(
        declarative_base=Base
    )
    automapped.prepare(autoload_with=conn.engine,)
    logging.info(f"MOD.1: automapped.classes={[orm_class.__name__ for orm_class in automapped.classes]}")
    return automapped