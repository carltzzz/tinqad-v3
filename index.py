from dash import dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
 
import dash 
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate 

import webbrowser 
from urllib.parse import urlparse, parse_qs
from flask import session

from app import app
from apps import commonmodules as cm
from apps import home
from apps import blankpage  
from apps import dbconnect as db

from apps.maindashboard import homepage, peer_evaluation_landing, peer_evaluation_form_entry, peer_evaluation_results, user_profile, register_user, search_users, password, about_TINQAD, basichome
from apps.director import peer_evaluation_settings, peer_evaluation_form, peer_evaluation_responses, evaluation_summary, remove_periods, director_dashboard
from apps.admin import add_inventory, administration_dashboard, expensetype_add, inventory_tracker, record_expenses, staff_profiles_management, staff_profiles, training_instructions, instructions, training_documents, add_expenses, training_record, viewexpense_list, viewtraining_list
from apps.iqa import iqa_dashboard, more_details, acad_heads_directory, acadheads_profile, iso_facilitator_directory, iso_facilitator_profile
from apps.eqa import eqa_dashboard, assessment_reports, assessment_details, accreditation_tracker, program_list, program_details, sar_details, program_info
from apps.eqa import program_page, reports_details
from apps.km import (km_dashboard, add_criteria, sdglist, sdg_form_1, sdg_form_2, sdg_form_3, sdg_form_4, sdg_form_5, sdg_form_6, sdg_form_7, sdg_form_8, sdg_form_9, sdg_form_10, sdg_form_11, sdg_form_12, sdg_form_13, sdg_form_14, sdg_form_15, sdg_form_16, sdg_form_17, qsrankings, qsrankingsprovider, sdg_QAO_view, sdg_1_evidence, sdg_2_evidence,
                     sdg_3_evidence, sdg_4_evidence, sdg_5_evidence, sdg_6_evidence, sdg_7_evidence, sdg_8_evidence, sdg_9_evidence, sdg_10_evidence, sdg_11_evidence, sdg_12_evidence,
                     sdg_13_evidence, sdg_14_evidence, sdg_15_evidence, sdg_16_evidence, sdg_17_evidence)
from apps.qaofficers import qa_directory, qaofficers_profile, training_details, qa_dashboard, faculty_cdf   


 
CONTENT_STYLE = {
    "margin-top": "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

server = app.server

# route tables
# Accessible to ALL authenticated users (accesstype >= 1)
SHARED_ROUTES = {
    '/profile': user_profile.layout,
    '/About_TINQAD': about_TINQAD.layout,
    # '/training_instructions': training_instructions.layout,
    # '/training_documents': training_documents.layout,
    '/km_dashboard': km_dashboard.layout,
    '/sdglist': sdglist.layout,
    '/sdglist/sdg1submission': sdg_form_1.layout,
    '/sdglist/sdg2submission': sdg_form_2.layout,
    '/sdglist/sdg3submission': sdg_form_3.layout,
    '/sdglist/sdg4submission': sdg_form_4.layout,
    '/sdglist/sdg5submission': sdg_form_5.layout,
    '/sdglist/sdg6submission': sdg_form_6.layout,
    '/sdglist/sdg7submission': sdg_form_7.layout,
    '/sdglist/sdg8submission': sdg_form_8.layout,
    '/sdglist/sdg9submission': sdg_form_9.layout,
    '/sdglist/sdg10submission': sdg_form_10.layout,
    '/sdglist/sdg11submission': sdg_form_11.layout,
    '/sdglist/sdg12submission': sdg_form_12.layout,
    '/sdglist/sdg13submission': sdg_form_13.layout,
    '/sdglist/sdg14submission': sdg_form_14.layout,
    '/sdglist/sdg15submission': sdg_form_15.layout,
    '/sdglist/sdg16submission': sdg_form_16.layout,
    '/sdglist/sdg17submission': sdg_form_17.layout,
}

# accesstype >= 2, needs to clarify pa the difference between accesses
ELEVATED_ROUTES = {
    '/register_user': register_user.layout,
    '/search_users': search_users.layout,
    '/password': password.layout,
    '/administration_dashboard': administration_dashboard.layout,
    '/record_expenses': record_expenses.layout,
    '/record_expenses/add_expense': add_expenses.layout,
    '/expense_list': viewexpense_list.layout,
    '/expense_list/add_expensetype': expensetype_add.layout,
    # '/instructions': instructions.layout,
    # '/training_record': training_record.layout,
    # '/training_record/mode=view': viewtraining_list.layout,
    '/inventory_tracker': inventory_tracker.layout,
    '/inventory_tracker_management': add_inventory.layout,
    '/staff_profiles': staff_profiles.layout,
    '/staff_profiles_management': staff_profiles_management.layout,
    '/peer_evaluation_landing': peer_evaluation_landing.main_layout,
    '/peer_evaluation_form_entry': peer_evaluation_form_entry.main_layout,
    '/peer_evaluation_results': peer_evaluation_results.layout,
    '/iqa_dashboard': iqa_dashboard.layout,
    '/dashboard/more_details': more_details.layout,
    '/acad_heads_directory': acad_heads_directory.layout,
    '/acadheads_profile': acadheads_profile.layout,
    '/iso_facilitator_directory': iso_facilitator_directory.layout,
    '/iso_facilitator_profile': iso_facilitator_profile.layout,
    '/eqa_dashboard': eqa_dashboard.layout,
    '/assessment_reports': assessment_reports.layout,
    '/assessment_tracker/assessment_details': assessment_details.layout,
    '/assessmentreports/sar_details': sar_details.layout,
    '/assessmentreports/reports_details': reports_details.layout,
    '/assessment_tracker': accreditation_tracker.layout,
    '/program_list': program_list.layout,
    '/program_details': program_details.layout,
    '/program_info': program_info.layout,
    '/program_page': program_page.layout,
    '/add_criteria': add_criteria.layout,
    '/SDG_evidencelist': sdg_QAO_view.layout,
    '/SDG_evidencelist/sdg1': sdg_1_evidence.layout,
    '/SDG_evidencelist/sdg2': sdg_2_evidence.layout,
    '/SDG_evidencelist/sdg3': sdg_3_evidence.layout,
    '/SDG_evidencelist/sdg4': sdg_4_evidence.layout,
    '/SDG_evidencelist/sdg5': sdg_5_evidence.layout,
    '/SDG_evidencelist/sdg6': sdg_6_evidence.layout,
    '/SDG_evidencelist/sdg7': sdg_7_evidence.layout,
    '/SDG_evidencelist/sdg8': sdg_8_evidence.layout,
    '/SDG_evidencelist/sdg9': sdg_9_evidence.layout,
    '/SDG_evidencelist/sdg10': sdg_10_evidence.layout,
    '/SDG_evidencelist/sdg11': sdg_11_evidence.layout,
    '/SDG_evidencelist/sdg12': sdg_12_evidence.layout,
    '/SDG_evidencelist/sdg13': sdg_13_evidence.layout,
    '/SDG_evidencelist/sdg14': sdg_14_evidence.layout,
    '/SDG_evidencelist/sdg15': sdg_15_evidence.layout,
    '/SDG_evidencelist/sdg16': sdg_16_evidence.layout,
    '/SDG_evidencelist/sdg17': sdg_17_evidence.layout,
    '/qs_rankings': qsrankings.layout,
    '/QAOfficers_dashboard': qa_dashboard.layout,
    '/qaofficers_profile': qaofficers_profile.layout,
    '/qaofficers_training': training_details.layout,
    '/qaofficers_directory': qa_directory.layout,
    '/qaofficers_faculty_cdf': faculty_cdf.layout,
}

# requires exact minimum role: {pathname: (min_role, layout)}
ROLE_RESTRICTED = {
    '/director_dashboard': (2, director_dashboard.layout),
    '/peer_evaluation_settings': (2, peer_evaluation_settings.layout),
    '/peer_evaluation_settings/peer_evaluation_forms': (2, peer_evaluation_form.layout),
    '/peer_evaluation_responses': (2, peer_evaluation_responses.layout),
    '/peer_evaluation_responses/evaluation_summary': (2, evaluation_summary.layout),
    '/peer_evaluation_settings/remove_evaluation_periods': (2, remove_periods.layout),
}

# basic-only routes (accesstype == 1)
BASIC_ONLY_ROUTES = {
    '/qs_rankings_provider': qsrankingsprovider.layout,
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),

        # LOGIN DATA
        # 1 current_user_id -- stores user_id
        dcc.Store(id='sessionlogout', data = True, storage_type='session'),
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 2 currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=0, storage_type='session'),
        
        # Page mode and user id for viewing for those that have any
        dcc.Store(id='page_mode', data=-1, storage_type='memory'),
        dcc.Store(id='view_id', data=-1, storage_type='memory'),

        cm.navbar,
        html.Div(id='page-content', style=CONTENT_STYLE),
        html.Link(rel='icon', href='/assets/icons/TINQAD.png')
    ]
)



@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
        State('currentrole', 'data'),
        State('url', 'search')
    ]
)
def displaypage(pathname, sessionlogout, user_id, accesstype, search):
    # Default return layout is a blank page
    returnlayout = blankpage.layout
    logout_conditions = [
        pathname in ['/', '/logout'],
        user_id == -1,
        not user_id
    ]
    sessionlogout = any(logout_conditions)

    # Server-side session validation
    sess_user_id = session.get('user_id')
    sess_access_type = session.get('access_type')

    # public pages can be accessed by everyone
    if pathname in ['/', '/home', '/logout']:
        if pathname in ['/', '/logout']:
            session.clear()
            sessionlogout = True
        returnlayout = home.layout
        return [returnlayout, sessionlogout]

    # protected pages require valid server session
    if sess_user_id is None:
        session.clear()
        return [home.layout, True]

    accesstype = sess_access_type
    sessionlogout = False

    # Parse mode from the URL search string if present
    mode = None
    parsed = urlparse(search)
    if parse_qs(parsed.query):
        mode = parse_qs(parsed.query).get('mode', [None])[0]

    # Check if the callback was triggered by the URL input
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    if eventid == 'url':
        if pathname == '/homepage':
            returnlayout = homepage.layout if accesstype >= 2 else basichome.layout
        elif pathname in SHARED_ROUTES:
            returnlayout = SHARED_ROUTES[pathname]
        elif accesstype == 1:
            returnlayout = BASIC_ONLY_ROUTES.get(pathname, blankpage.layout)
        elif accesstype >= 2:
            if pathname in ROLE_RESTRICTED:
                required_role, layout = ROLE_RESTRICTED[pathname]
                if accesstype == required_role:
                    returnlayout = layout
            else:
                returnlayout = ELEVATED_ROUTES.get(pathname, blankpage.layout)

    return [returnlayout, sessionlogout]
if __name__ == '__main__':
   webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
   app.run(debug=False)

# if __name__ == '__main__':
#     # Open the web browser to the correct URL 
#     url = 'http://10.206.100.41:8050/'
#     webbrowser.open(url, new=0, autoraise=True)
    
#     # Run the Dash app on all network interfaces (0.0.0.0) on port 8050
#     app.run_server(host='10.206.100.41', port=8050, debug=False)