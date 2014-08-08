# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from translator.toscalib.elements.constraints import Constraint


class Property(object):
    '''TOSCA built-in Property type.'''

    PROPERTY_KEYS = (
        TYPE, REQUIRED, DESCRIPTION, DEFAULT, CONSTRAINTS,
    ) = (
        'type', 'required', 'description', 'default', 'constraints'
    )

    def __init__(self, property_name, value, schema=None):
        self.name = property_name
        self.value = value
        self.schema = schema

    @property
    def constraints(self):
        try:
            if self.CONSTRAINTS in self.schema:
                return self.schema[self.CONSTRAINTS]
        except Exception:
            #Simply passing the exception to ignore Node Type in-line value.
            #Exception will not be needed when Node Type and Node Template
            #properties are separated.
            #TODO(spzala)
            pass

    @property
    def description(self):
        if self.schema:
            if self.DESCRIPTION in self.schema:
                return self.schema[self.DESCRIPTION]
        return ''

    def validate(self):
        '''Validate if not a reference property.'''
        if not isinstance(self.value, dict):
            self._validate_datatype()
            self._validate_constraints()

    def _validate_datatype(self):
        try:
            if self.TYPE in self.schema:
                dtype = self.schema[self.TYPE]
                if dtype == Constraint.STRING:
                    return Constraint.validate_string(self.value)
                elif dtype == Constraint.INTEGER:
                    return Constraint.validate_integer(self.value)
                elif dtype == Constraint.NUMBER:
                    return Constraint.validate_number(self.value)
                elif dtype == Constraint.LIST:
                    return Constraint.validate_list(self.value)
        except Exception:
            pass

    def _validate_constraints(self):
        constraints = self.constraints
        dtype = self.schema[self.TYPE]
        if constraints:
            for constraint in constraints:
                Constraint(self.name, dtype,
                           constraint).validate(self.value)