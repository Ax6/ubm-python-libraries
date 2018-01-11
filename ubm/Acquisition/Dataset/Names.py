"""
Throttle	P_Oil	P_Air	P_Rail	TAirLM35	TH2OLM35
Lambdacyl1UF	Lambdacyl2UF	Lambdacyl3UF	Lambdacyl4UF
dtcalcus	RUN	ECUCPU	ECUMemory	ECUDisk	ECUChassisC	TH2OC	TAIRC	TFUELC	TOILC
CutOff	FilmCompensation	TorqueReduction	UserCorrection	Idle	LambdaCtrl
SAmapcyl1	SAmapcyl2	SAmapcyl3	SAmapcyl4
SAactcyl1	SAactcyl2	SAactcyl3	SAactcyl4
dtSATCScyl1	dtSATCScyl2	dtSATCScyl3	dtSATCScyl4
dtSAidlecyl1	dtSAidlecyl2	dtSAidlecyl3	dtSAidlecyl4
SAstartcyl1	SAstartcyl2	SAstartcyl3	SAstartcyl4
MjopenLoopCyl1	MjopenLoopCyl2	MjopenLoopCyl3	MjopenLoopCyl4
Mjfilmcyl1	Mjfilmcyl2	Mjfilmcyl3	Mjfilmcyl4
Mjactcyl1	Mjactcyl2	Mjactcyl3	Mjactcyl4
Tjactcyl1	Tjactcyl2	Tjactcyl3	Tjactcyl4
Mjstartcyl1	Mjstartcyl2	Mjstartcyl3	Mjstartcyl4
dtSAcyl14CA	dtSAcyl23CA
corrMjcyl1kMj	corrMjcyl2kMj	corrMjcyl3kMj	corrMjcyl4kMj
RPM	AngEvapWarning	Cycles	SMOTnoise	SYNClost	LambdaTargetact
AngEvapCA	SCAMnoise	dtSMOT
LambdaCtrlcorrcyl1	LambdaCtrlcorrcyl2	LambdaCtrlcorrcyl3	LambdaCtrlcorrcyl4
TCK1C	TCK2C	PacketNumber
Lambdacyl1	Lambdacyl2	Lambdacyl3	Lambdacyl4
TorqueReductionact	actMap
TScamb1	TScamb2	TCool1	TCool2	TCool3
FuelPump	H2OPump	Fan	Brake	Spare2
GearUP	GearDOWN
StartEN	VCUCPU	VCUMemory	VCUDisk
ChassisC	LapNumber	LapTime
SpeedFLKmh	SpeedFRKmh	SpeedRLKmh	SpeedRRKmh
Gear	Upshifts	Downshifts	TCSAct	LCSAct
AccTimems	AccFinSpeedKmh	SlipSX	SlipDX	Warning	GPSWITCH	SteeringAngle
FRHeightmm	FLHeightmm
PPneumBar	PbrakeFrontBar	PbrakeRearBar	ClutchPosPneum
BatteryCurrentA	BatteryVoltageV
RRHeightmm	RLHeightmm
AccXg	AccYg	AccZg
GyroXrad	GyroYrad	GyroZrad
ClutchPaddle
DamperFLmm	DamperFRmm	DamperRLmm	DamperRRmm
"""


class Names:
    """
    Another Luke pearl
    """

    # (Right, Wrong)
    COMPATIBILITY_DICTIONARY = [
        ('DamperFLmm', 'DamperFL'),
        ('DamperFRmm', 'DamperFR'),
        ('DamperRLmm', 'DamperRL'),
        ('DamperRRmm', 'DamperRR'),
    ]

    Driver = {
        "SteeringAngle": 'SteeringAngle',
        "Throttle": 'Throttle',
        "Brakes": ('PbrakeFrontBar', 'PbrakeRearBar')
    }

    Engine = {

    }

    IMU = {
        "Accelerometer": ('AccXg', 'AccYg', 'AccZg'),
        "Gyroscope": ('GyroXrad', 'GyroYrad', 'GyroZrad')
    }

    Internal = {

    }

    Vehicle = {
        "PhonicWheels": ('SpeedFLKmh', 'SpeedFRKmh', 'SpeedRLKmh', 'SpeedRRKmh'),
        "Dampers": ('DamperFLmm', 'DamperFRmm', 'DamperRLmm', 'DamperRRmm'),
        "RideHeight": ('FLHeightmm', 'FRHeightmm', 'RLHeightmm', 'RRHeightmm')
    }

    def __init__(self):
        return

    def fix(self, dataset):
        for right, wrong in self.COMPATIBILITY_DICTIONARY:
            if wrong in dataset.get_original_data().columns:
                dataset.original_data[right] = dataset.original_data[wrong]
                dataset.original_data[wrong] = None
