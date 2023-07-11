import 'package:app/models/AirIntake.dart';
import 'package:app/models/RunTime.dart';
import 'package:app/models/RPM.dart';
import 'package:app/models/Speed.dart';
import 'package:app/models/Throttle.dart';

class Data {
  final RunTime runTime;
  final String fuelType;
  final Throttle throttle;
  final AirIntake airIntake;
  final RPM rpm;
  final Speed speed;
  final String ethanolPercentage;
  final double fuelEfficiency;

  Data({
    required this.runTime,
    required this.fuelType,
    required this.throttle,
    required this.airIntake,
    required this.rpm,
    required this.speed,
    required this.ethanolPercentage,
    required this.fuelEfficiency,
  });

  factory Data.fromJson(Map<String, dynamic> json) {
    return Data(
      runTime: RunTime.fromJson(json['Run Time']),
      fuelType: json['Fuel Type'],
      throttle: Throttle.fromJson(json['Throttle']),
      airIntake: AirIntake.fromJson(json['Air Intake']),
      rpm: RPM.fromJson(json['RPM']),
      speed: Speed.fromJson(json['Speed']),
      ethanolPercentage: json['Ethanol %'],
      fuelEfficiency: json['Fuel Efficiency'].toDouble() * 100,
    );
  }
}
