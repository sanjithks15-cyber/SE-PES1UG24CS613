import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


def make_ward(patients, accepting=True, tier="general", icu=False):
    return {
        "is_accepting": accepting,
        "tier": tier,
        "icu_standby": icu,
        "patients": patients,
    }


# ---------- process_triage_wards: input validation ----------
def test_single_normal_patient():
    result = process_triage_wards([make_ward([{"spo2": 98, "hr": 72, "unconscious": False}])], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_invalid_wards_not_a_list():
    with pytest.raises(ValueError):
        process_triage_wards("not-a-list", 10)


def test_invalid_negative_default_score():
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_zero_default_score_is_valid():
    assert process_triage_wards([make_ward([{"spo2": 98, "hr": 72}])], 0)["status"] == "NO_URGENT_CASES"


# ---------- process_triage_wards: ward-level branches ----------
def test_ward_not_accepting_is_skipped():
    result = process_triage_wards([make_ward([{"spo2": 80, "hr": 130}], accepting=False)], 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_ward_missing_is_accepting_key_defaults_to_skipped():
    assert process_triage_wards([{"patients": [{"spo2": 98}]}], 10)["status"] == "NO_URGENT_CASES"


def test_ward_defaults_for_missing_keys():
    # accepting ward with no tier / patients / icu_standby keys
    result = process_triage_wards([{"is_accepting": True}], 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_empty_wards_list():
    assert process_triage_wards([], 10) == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_icu_standby_true_adds_bonus():
    assert process_triage_wards([make_ward([{"spo2": 98, "hr": 72}], icu=True)], 10)["acuity_score"] == 35


def test_icu_standby_false_no_bonus():
    assert process_triage_wards([make_ward([{"spo2": 98, "hr": 72}], icu=False)], 10)["acuity_score"] == 10


# ---------- process_triage_wards: patient-level branches ----------
def test_patient_defaults_use_normal_vitals():
    assert process_triage_wards([make_ward([{}])], 10)["acuity_score"] == 10


def test_spo2_zero_flagged():
    result = process_triage_wards([make_ward([{"spo2": 0, "hr": 70}])], 10)
    assert result["acuity_score"] == 0


def test_heart_rate_zero_flagged_with_valid_spo2():
    result = process_triage_wards([make_ward([{"spo2": 95, "hr": 0}])], 10)
    assert result["acuity_score"] == 0


def test_unconscious_general_ward_adds_100():
    result = process_triage_wards([make_ward([{"unconscious": True}])], 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_outpatient_resets_and_breaks():
    wards = [make_ward([{"spo2": 98}, {"unconscious": True}, {"spo2": 98}], tier="outpatient")]
    assert process_triage_wards(wards, 10) == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_conscious_outpatient_scored_normally():
    assert process_triage_wards([make_ward([{"spo2": 98}], tier="outpatient")], 10)["acuity_score"] == 10


def test_low_spo2_adds_60():
    assert process_triage_wards([make_ward([{"spo2": 89, "hr": 80}])], 10)["acuity_score"] == 60


def test_high_heart_rate_adds_60():
    assert process_triage_wards([make_ward([{"spo2": 95, "hr": 121}])], 10)["acuity_score"] == 60


def test_boundary_values_are_normal():
    # spo2 == 90 and hr == 120 are not abnormal
    assert process_triage_wards([make_ward([{"spo2": 90, "hr": 120}])], 10)["acuity_score"] == 10


def test_multiple_wards_accumulate():
    wards = [
        make_ward([{"spo2": 98}], icu=True),
        make_ward([{"spo2": 85}], accepting=False),
        make_ward([{"hr": 150}]),
    ]
    assert process_triage_wards(wards, 10)["acuity_score"] == 10 + 25 + 60


# ---------- process_triage_wards: final status branches ----------
def test_ward_alert_when_more_than_four_flagged():
    result = process_triage_wards([make_ward([{"spo2": 0}] * 5)], 10)
    assert result == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_four_flagged_is_not_alert():
    result = process_triage_wards([make_ward([{"spo2": 0}] * 4)], 10)
    assert result["status"] == "NO_URGENT_CASES"


def test_ward_alert_keeps_accumulated_score():
    patients = [{"unconscious": True}] * 5
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": 500, "status": "WARD_ALERT"}


# ---------- monitor_oxygen_manifolds ----------
def test_oxygen_no_data_empty_list():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_no_data_none():
    assert monitor_oxygen_manifolds(None) == "NO_DATA"


def test_oxygen_pressure_failure_two_consecutive_drops():
    assert monitor_oxygen_manifolds([[5.0, 3.0, 3.5]]) == "PRESSURE_FAILURE"


def test_oxygen_single_drop_is_normal():
    assert monitor_oxygen_manifolds([[5.0, 3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_streak_resets_between_drops():
    assert monitor_oxygen_manifolds([[3.0, 5.0, 3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_streak_resets_per_manifold():
    assert monitor_oxygen_manifolds([[3.0], [3.0]]) == "PRESSURE_NORMAL"


def test_oxygen_failure_in_later_manifold():
    assert monitor_oxygen_manifolds([[5.0, 5.0], [3.9, 3.9]]) == "PRESSURE_FAILURE"


def test_oxygen_empty_manifold_is_normal():
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"


def test_oxygen_exactly_four_bar_is_normal():
    assert monitor_oxygen_manifolds([[4.0, 4.0]]) == "PRESSURE_NORMAL"
