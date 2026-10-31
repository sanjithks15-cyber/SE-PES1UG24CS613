import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, accepting=True, tier="general", icu=False):
    return {
        "is_accepting": accepting,
        "tier": tier,
        "icu_standby": icu,
        "patients": patients,
    }


def test_single_normal_patient():
    result = process_triage_wards([make_ward([{"spo2": 98, "hr": 72, "unconscious": False}])], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_invalid_wards_not_a_list():
    with pytest.raises(ValueError):
        process_triage_wards("not-a-list", 10)


def test_invalid_negative_default_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_ward_not_accepting_is_skipped():
    result = process_triage_wards([make_ward([{"spo2": 80, "hr": 130}], accepting=False)], 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_vitals_are_flagged_and_skipped():
    wards = [make_ward([{"spo2": 0, "hr": 70}, {"spo2": 95, "hr": 0}])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_unconscious_patient_general_ward():
    result = process_triage_wards([make_ward([{"unconscious": True}])], 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_patient_outpatient_resets_score():
    wards = [make_ward([{"spo2": 98, "hr": 72}, {"unconscious": True}, {"spo2": 98}], tier="outpatient")]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_low_spo2_patient():
    result = process_triage_wards([make_ward([{"spo2": 85, "hr": 80}])], 10)
    assert result["acuity_score"] == 60


def test_high_heart_rate_patient():
    result = process_triage_wards([make_ward([{"spo2": 95, "hr": 130}])], 10)
    assert result["acuity_score"] == 60


def test_icu_standby_bonus():
    result = process_triage_wards([make_ward([{"spo2": 98, "hr": 72}], icu=True)], 10)
    assert result["acuity_score"] == 35


def test_ward_alert_when_many_flagged_entries():
    wards = [make_ward([{"spo2": 0}] * 5)]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"


def test_oxygen_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_pressure_failure():
    assert monitor_oxygen_manifolds([[5.0, 3.0, 3.5]]) == "PRESSURE_FAILURE"


def test_oxygen_pressure_normal():
    assert monitor_oxygen_manifolds([[5.0, 4.5]]) == "PRESSURE_NORMAL"
