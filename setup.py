#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Noah Kantrowitz <noah@coderanger.net>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from setuptools import setup

setup(
    name='GanttTicketEdit',
    version='1.0',
    packages=['gantt_ticket_edit'],
    package_data={'gantt_ticket_edit': ['templates/*']},

    author='Artem Kondratyev',
    author_email='konapt@gmail.com',
    description='A module that provides ticket edit form for Gantt page.',
    license='BSD 3-Clause',
    keywords='trac plugin ticket gantt',
    url='http://trac-hacks.org/wiki/',
    classifiers=[
        'Framework :: Trac',
    ],

    install_requires=['Trac>=0.11'],
    extras_require={'ticketcalendarplugin': 'TicketCalendarPlugin'},

    entry_points={
        'trac.plugins': [
            'gantt_ticket_edit.web_ui = gantt_ticket_edit.web_ui',
        ]
    },
)