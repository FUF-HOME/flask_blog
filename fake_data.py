#!/usr/bin/env python
# -*-coding:utf-8-*-
from app.models import db, Tag

tag_one = Tag(name='Python')
tag_two = Tag(name='Flask')
tag_three = Tag(name='SQLALchemy')
tag_four = Tag(name='FuF')
tag_list = [tag_one, tag_two, tag_three, tag_four]
for i in tag_list:
    db.session.add(i)
db.session.commit()
