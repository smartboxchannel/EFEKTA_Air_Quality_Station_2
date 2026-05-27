from enum import Enum
from typing import Final

from zigpy.profiles import zha
from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import (
    QuirkBuilder,
    SensorDeviceClass,
    SensorStateClass,
    EntityType,
    EntityPlatform,
)
from zigpy.quirks.v2.homeassistant.number import NumberDeviceClass
import zigpy.types as t
from zigpy.zcl import ClusterType
from zigpy.zcl.foundation import ZCLAttributeDef
from zigpy.zcl.clusters.general import Basic, AnalogInput
from zigpy.zcl.clusters.measurement import (
    CarbonDioxideConcentration,
    FormaldehydeConcentration,
    RelativeHumidity,
    TemperatureMeasurement,
    PM25,
    IlluminanceMeasurement,
)
from zigpy.quirks.v2.homeassistant import (
    UnitOfTime,
    UnitOfTemperature,
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    UnitOfLength,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

def round_to_one(value: float) -> float:
    return round(value, 1)
    
def round_to_zero(value: float) -> float:
    return round(value, 0)
    
def round_to_two(value: float) -> float:
    return round(value, 2)

EFEKTA = "EfektaLab"

    
class VOCIndex(AnalogInput, CustomCluster):
    name: str = "VOC Index"
    ep_attribute: str = "voc_index"
    class AttributeDefs(AnalogInput.AttributeDefs):
        nox_index: Final = ZCLAttributeDef(id=0x0155, type=t.Single, access="r")
    
class PMMeasurement(PM25, CustomCluster):
    class AttributeDefs(PM25.AttributeDefs):
        pm1: Final = ZCLAttributeDef(id=0x0601, type=t.Single, access="r")
        pm4: Final = ZCLAttributeDef(id=0x0605, type=t.Single, access="r")
        pm10: Final = ZCLAttributeDef(id=0x0602, type=t.Single, access="r")
        pm_size: Final = ZCLAttributeDef(id=0x0603, type=t.Single, access="r")
        pmN05: Final = ZCLAttributeDef(id=0x0640, type=t.Single, access="r")
        pmN1: Final = ZCLAttributeDef(id=0x0641, type=t.Single, access="r")
        pmN25: Final = ZCLAttributeDef(id=0x0642, type=t.Single, access="r")
        pmN4: Final = ZCLAttributeDef(id=0x0643, type=t.Single, access="r")
        pmN10: Final = ZCLAttributeDef(id=0x0644, type=t.Single, access="r")
        auto_clean_interval: Final = ZCLAttributeDef(id=0x0330, type=t.uint8_t, access="rw")
        manual_clean: Final = ZCLAttributeDef(id=0x0331, type=t.Bool, access="rw")
        report_delay: Final = ZCLAttributeDef(id=0x0201, type=t.uint16_t, access="rw")
        
class CO2Measurement(CarbonDioxideConcentration, CustomCluster):
    class AttributeDefs(CarbonDioxideConcentration.AttributeDefs):
        set_altitude: Final = ZCLAttributeDef(id=0x0205, type=t.uint16_t, access="rw")
        forced_recalibration: Final = ZCLAttributeDef(id=0x0202, type=t.Bool, access="rw")
        manual_forced_recalibration: Final = ZCLAttributeDef(id=0x0207, type=t.uint16_t, access="rw")
        automatic_self_calibration: Final = ZCLAttributeDef(id=0x0402, type=t.Bool, access="rw")
        factory_reset_co2: Final = ZCLAttributeDef(id=0x0206, type=t.Bool, access="rw")
        
class IlluminanceMeasurementExt(IlluminanceMeasurement, CustomCluster):
    class AttributeDefs(IlluminanceMeasurement.AttributeDefs):
        auto_brightness: Final = ZCLAttributeDef(id=0x0203, type=t.Bool, access="rw")
        night_onoff_backlight: Final = ZCLAttributeDef(id=0x0401, type=t.Bool, access="rw")
        night_on_backlight: Final = ZCLAttributeDef(id=0x0405, type=t.uint8_t, access="rw")
        night_off_backlight: Final = ZCLAttributeDef(id=0x0406, type=t.uint8_t, access="rw")

class TempMeasurement(TemperatureMeasurement, CustomCluster):
    class AttributeDefs(TemperatureMeasurement.AttributeDefs):
        temperature_offset: Final = ZCLAttributeDef(id=0x0210, type=t.int16s, access="rw")


class RHMeasurement(RelativeHumidity, CustomCluster):
    class AttributeDefs(RelativeHumidity.AttributeDefs):
        humidity_offset: Final = ZCLAttributeDef(id=0x0210, type=t.int16s, access="rw")
        
(
    QuirkBuilder(EFEKTA, "EFEKTA_Air_Quality_Station_2")
    .replaces_endpoint(1, device_type=zha.DeviceType.SIMPLE_SENSOR)
    .replaces_endpoint(2, device_type=zha.DeviceType.SIMPLE_SENSOR)
    .replaces_endpoint(3, device_type=zha.DeviceType.SIMPLE_SENSOR)
    .replaces(Basic, endpoint_id=1)
    .replaces(PMMeasurement, endpoint_id=1)
    .replaces(CO2Measurement, endpoint_id=2)
    .replaces(IlluminanceMeasurementExt, endpoint_id=2)
    .replaces(VOCIndex, endpoint_id=3)
    .replaces(TempMeasurement, endpoint_id=3)
    .replaces(RHMeasurement, endpoint_id=3)
    .skip_configuration(True)
    .sensor(
        PMMeasurement.AttributeDefs.pm1.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM1,
        translation_key="pm1",
        fallback_name="PM1",
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        attribute_converter=round_to_two,
    )
    .sensor(
        PMMeasurement.AttributeDefs.measured_value.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pm25",
        fallback_name="PM2.5",
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        attribute_converter=round_to_two,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pm4.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pm4",
        fallback_name="PM4",
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        attribute_converter=round_to_two,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pm10.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM10,
        translation_key="pm10",
        fallback_name="PM10",
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        attribute_converter=round_to_two,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pm_size.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pm_size",
        fallback_name="Typical Particle Size",
        unit="µm",
        attribute_converter=round_to_two,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pmN05.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pmN05",
        fallback_name="PM#0.5",
        unit="#/cm³",
        attribute_converter=round_to_zero,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pmN1.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pmN1",
        fallback_name="PM#1",
        unit="#/cm³",
        attribute_converter=round_to_zero,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pmN25.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pmN25",
        fallback_name="PM#2.5",
        unit="#/cm³",
        attribute_converter=round_to_zero,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pmN4.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pmN4",
        fallback_name="PM#4",
        unit="#/cm³",
        attribute_converter=round_to_zero,
    )
    .sensor(
        PMMeasurement.AttributeDefs.pmN10.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.PM25,
        translation_key="pmN10",
        fallback_name="PM#10",
        unit="#/cm³",
        attribute_converter=round_to_zero,
    )
    .sensor(
        VOCIndex.AttributeDefs.present_value.name,
        VOCIndex.cluster_id,
        endpoint_id=3,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.AQI,
        translation_key="voc_index",
        fallback_name="VOC Index",
    )
    .sensor(
        VOCIndex.AttributeDefs.nox_index.name,
        VOCIndex.cluster_id,
        endpoint_id=3,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.AQI,
        translation_key="nox_index",
        fallback_name="NOX Index",
    )
    .number(
        TempMeasurement.AttributeDefs.temperature_offset.name,
        TempMeasurement.cluster_id,
        endpoint_id=3,
        translation_key="temperature_offset",
        fallback_name="Adjust temperature",
        unique_id_suffix="temperature_offset",
        min_value=-50,
        max_value=50,
        step=0.1,
        multiplier=0.1,
        device_class=NumberDeviceClass.TEMPERATURE,
        unit=UnitOfTemperature.CELSIUS,
        mode="box",
    )
    .number(
        RHMeasurement.AttributeDefs.humidity_offset.name,
        RHMeasurement.cluster_id,
        endpoint_id=3,
        translation_key="humidity_offset",
        fallback_name="Adjust humidity",
        unique_id_suffix="humidity_offset",
        min_value=-50,
        max_value=50,
        step=1,
        device_class=NumberDeviceClass.HUMIDITY,
        unit=PERCENTAGE,
        mode="box",
    )
    .number(
        PMMeasurement.AttributeDefs.auto_clean_interval.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        translation_key="auto_clean_interval",
        fallback_name="Auto Clean Interval",
        unique_id_suffix="auto_clean_interval",
        min_value=0,
        max_value=10,
        step=1,
        device_class=SensorDeviceClass.DURATION,
        unit=UnitOfTime.DAYS,
    )
    .switch(
        PMMeasurement.AttributeDefs.manual_clean.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        translation_key="manual_clean",
        fallback_name="Manual Clean",
        unique_id_suffix="manual_clean",
    )
    .number(
        PMMeasurement.AttributeDefs.report_delay.name,
        PMMeasurement.cluster_id,
        endpoint_id=1,
        translation_key="report_delay",
        fallback_name="Report delay",
        unique_id_suffix="report_delay",
        min_value=6,
        max_value=600,
        step=1,
        device_class=NumberDeviceClass.DURATION,
        unit=UnitOfTime.SECONDS,
    )
    .switch(
        IlluminanceMeasurementExt.AttributeDefs.auto_brightness.name,
        IlluminanceMeasurementExt.cluster_id,
        endpoint_id=2,
        translation_key="auto_brightness",
        fallback_name="Auto brightness",
        unique_id_suffix="auto_brightness",
    )
    .switch(
        IlluminanceMeasurementExt.AttributeDefs.night_onoff_backlight.name,
        IlluminanceMeasurementExt.cluster_id,
        endpoint_id=2,
        translation_key="night_onoff_backlight",
        fallback_name="Night ON|OFF backlight",
        unique_id_suffix="night_onoff_backlight",
    )
    .number(
        IlluminanceMeasurementExt.AttributeDefs.night_on_backlight.name,
        IlluminanceMeasurementExt.cluster_id,
        endpoint_id=2,
        translation_key="night_on_backlight",
        fallback_name="Night ON backlight",
        unique_id_suffix="night_on_backlight",
        min_value=0,
        max_value=23,
        step=1,
        device_class=NumberDeviceClass.DURATION,
        unit=UnitOfTime.HOURS,
    )
    .number(
        IlluminanceMeasurementExt.AttributeDefs.night_off_backlight.name,
        IlluminanceMeasurementExt.cluster_id,
        endpoint_id=2,
        translation_key="night_off_backlight",
        fallback_name="Night OFF backlight",
        unique_id_suffix="night_off_backlight",
        min_value=0,
        max_value=23,
        step=1,
        device_class=NumberDeviceClass.DURATION,
        unit=UnitOfTime.HOURS,
    )
    .switch(
        CO2Measurement.AttributeDefs.forced_recalibration.name,
        CO2Measurement.cluster_id,
        endpoint_id=2,
        translation_key="forced_recalibration",
        fallback_name="Start FRC (Perform Forced Recalibration of the CO2 Sensor)",
        unique_id_suffix="forced_recalibration",
    )
    .number(
        CO2Measurement.AttributeDefs.manual_forced_recalibration.name,
        CO2Measurement.cluster_id,
        endpoint_id=2,
        translation_key="manual_forced_recalibration",
        fallback_name="FRC",
        unique_id_suffix="manual_forced_recalibration",
        min_value=0,
        max_value=5000,
        step=1,
        unit=CONCENTRATION_PARTS_PER_MILLION,
    )
    .switch(
        CO2Measurement.AttributeDefs.automatic_self_calibration.name,
        CO2Measurement.cluster_id,
        endpoint_id=2,
        translation_key="automatic_self_calibration",
        fallback_name="Automatic self calibration",
        unique_id_suffix="automatic_self_calibration",
    )
    .switch(
        CO2Measurement.AttributeDefs.factory_reset_co2.name,
        CO2Measurement.cluster_id,
        endpoint_id=2,
        translation_key="factory_reset_co2",
        fallback_name="Factory Reset CO2 sensor",
        unique_id_suffix="factory_reset_co2",
    )
    .number(
        CO2Measurement.AttributeDefs.set_altitude.name,
        CO2Measurement.cluster_id,
        endpoint_id=2,
        translation_key="set_altitude",
        fallback_name="Set altitude",
        unique_id_suffix="set_altitude",
        min_value=0,
        max_value=3000,
        step=1,
        unit=UnitOfLength.METERS,
    )
    .add_to_registry()
)