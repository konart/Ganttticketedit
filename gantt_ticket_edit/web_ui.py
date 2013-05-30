# -*- coding: utf-8 -*- 

from trac.core import *
from trac.web.api import IRequestFilter, IRequestHandler
from trac.web.chrome import ITemplateProvider, add_script, add_stylesheet
from trac.config import *
import simplejson as json

class GanttTicketEdit(Component):
	"""A module that provides ticket edit form for Gantt page."""

	implements(IRequestFilter, IRequestHandler, ITemplateProvider)


		    # ITemplateProvider methods
	def get_htdocs_dirs(self):
		from pkg_resources import resource_filename
	#	return [('gantt_ticket_edit', resource_filename(__name__, 'htdocs'))]
   		return []

	def get_templates_dirs(self):
		from pkg_resources import resource_filename
		return [resource_filename(__name__, 'templates')]
	#	return []

			# IRequestFilter methods
	def pre_process_request(self, req, handler):
		return handler

	def post_process_request(self, req, template, data, content_type):
		if (req.path_info.startswith('/ticketgantt') and (req.perm.has_permission('TICKET_VIEW') or req.perm.has_permission('TICKET_MODIFY'))):
				#add_stylesheet(req, '/gantt_ticket_edit/style.css')
				add_script(req, '/gantt_ticket_edit/edit_form.js')
				
		return template, data, content_type

		# IRequestHandler methods
	def match_request(self, req):
		return req.path_info.startswith('/gantt_ticket_edit')
	   
	def process_request(self, req):
		
		if req.perm.has_permission('TICKET_MODIFY'):
			has_permission = json.dumps("True")

		filtered_options = []
		for option in self.options:
			if not Configuration.getbool(self.config,'GanttTicketEdit',option):
				filtered_options.append(option)
		filtered_options = json.dumps(filtered_options)

		return 'edit_form.js', {'options':filtered_options, 'has_permission':has_permission}, 'text/plain'


	# Options go here
	optional_fields = ['Summary', 'Reporter', 'Description', 'Type', 'Milestone', 
						'Keywords', 'Blocked By', 'Start date', 'Estimated Hours', 
						'Contact Person', '% Complete', 'Close date', 'Release date act', 
						'Tariff', 'Priority', 'Component', 'Cc', 'Blocking', 'Due Date', 'Total Hours', 
						'Contragent', "Performer's rating", 'Release date plan', 'Payment date']

	options = {}
	for field in optional_fields:
		options['field-'+field.replace(" ", "-").replace("'s","").replace("%-","").lower()] = BoolOption('GanttTicketEdit', 'field-'+field.replace (" ", "-").replace("'s","").replace("%-","").lower(), 'True', u'Отображать на форме поле "' + field + u'"?')
	