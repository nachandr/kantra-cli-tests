import os
import subprocess

from utils import constants
from utils.command import build_analysis_command
from utils.report import assert_insights_from_report_file, get_json_from_report_output_file

# Polarion TC 598
def test_insights_binary_app(analysis_data):
    application_data = analysis_data['jee_example_app']
 
    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target']
    )

    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout

    assert 'generating static report' in output
    assert_insights_from_report_file()

# Polarion TC 3504, 3505, 3506
def test_custom_rules(analysis_data):
    application_data = analysis_data['tackle-testapp-project']
    custom_rule_path = os.path.join(os.getenv(constants.PROJECT_PATH), 'data/yaml', 'custom_rule_insights.yaml')
 
    command = build_analysis_command(
        application_data['file_name'],
        application_data['source'],
        application_data['target'],
        **{'rules': custom_rule_path}
    )
 
    output = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    assert 'generating static report' in output
 
    report_data = get_json_from_report_output_file()
    for rule in report_data['rulesets']:
        insights = rule.get('insights', {})
 
        for insight in insights.values():
            if rule['name'] == 'custom-ruleset':
                if insight['description'] in ('Properties file (Insights TC0)', 'Properties file (Insights TC1)',
                    'Properties file (Insights TC2)'):
                    # Assert insight occurrence is > 0 for each insight
                    assert len(insight['incidents']) > 0, "No insights were generated"
