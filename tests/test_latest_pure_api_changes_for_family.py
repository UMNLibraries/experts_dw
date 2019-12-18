from experts_dw.sqlapi import sqlapi

def test_latest_pure_api_changes_for_family():
    change = next(
        sqlapi.latest_pure_api_changes_for_family(
            family_system_name='ResearchOutput'
        )
    )
    assert change['family_system_name'] == 'ResearchOutput'
