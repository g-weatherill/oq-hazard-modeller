# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2010-2011, GEM Foundation.
#
# OpenQuake is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# OpenQuake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with OpenQuake. If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.

"""
The purpose of this module is to provide objects
to read EQCatalogs in different formats such as:
csv, nrml.
"""

import os
import csv
from lxml import etree


class CsvReader(object):
    """
    CsvReader allows to read csv file in
    an iterative way, building a dictionary
    for every data line inside the csv file,
    dictionary's keys correspond to the csv
    fieldnames while dictionary values are the
    corresponding fieldname/column value.
    """

    def __init__(self, filename):
        file_exists = os.path.exists(filename)
        if not file_exists:
            raise IOError('File %s not found' % filename)
        self.filename = filename

    def read(self):
        """
        Return a generator that provides an EQ definition
        in a dictionary for each line of the file.
        """
        with open(self.filename, 'rb') as csv_file:
            reader = csv.reader(csv_file)
            reader.next()  # Skip the first line containing fieldnames
            for line in reader:
                eq_entry = dict(zip(self.fieldnames, line))
                yield eq_entry

    @property
    def fieldnames(self):
        """Return the fieldnames inside the csv file."""
        with open(self.filename, 'rb') as csv_file:
            reader = csv.DictReader(csv_file).fieldnames
        return reader

class XMLValidationError(Exception):
    """XML schema validation error"""

    def __init__(self, filename, message):
        """Constructs a new validation exception for the given file name"""
        self.args = (filename, message)
        self.filename = filename
        self.message = message

class SourceModelReader(object):
    """
    SourceModelReader allows to read source model in nrml
    file in an iterative way.
    """

    def __init__(self, filename, schema):
        file_exists = os.path.exists(filename)
        if not file_exists:
            raise IOError('File %s not found' % filename)
        if not SourceModelReader.valid_schema(filename, schema):
            raise XMLValidationError(filename, 'The source model doesn\'t conform to the schema')
        self.filename = filename
        self.schema = schema

    @staticmethod
    def valid_schema(source_model_path, schema_path):
        xml_doc = etree.parse(source_model_path)
        xmlschema = etree.XMLSchema(etree.parse(schema_path))
        return xmlschema.validate(xml_doc)
