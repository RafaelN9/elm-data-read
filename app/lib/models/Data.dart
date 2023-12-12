import 'package:app/models/MAF.dart';
import 'package:app/models/RunTime.dart';
import 'package:app/models/RPM.dart';
import 'package:app/models/Speed.dart';
import 'package:app/models/Throttle.dart';

class Data {
  final RunTime runTime;
  final String fuelType;
  final Throttle throttle;
  final MAF maf;
  final RPM rpm;
  final Speed speed;
  final double ethanolPercentage;
  final double loadPercentage;

  Data({
    required this.runTime,
    required this.fuelType,
    required this.throttle,
    required this.maf,
    required this.rpm,
    required this.speed,
    required this.ethanolPercentage,
    required this.loadPercentage,
  });

  factory Data.fromJson(Map<String, dynamic> json) {
    return Data(
      runTime: RunTime.fromJson(json['Run Time']),
      fuelType: json['Fuel Type'],
      throttle: Throttle.fromJson(json['Throttle']),
      maf: MAF.fromJson(json['MAF']),
      rpm: RPM.fromJson(json['RPM']),
      speed: Speed.fromJson(json['Speed']),
      ethanolPercentage: (json['Ethanol %'] != 'N/A') ? json['Ethanol %'] : 0.0,
      loadPercentage: (json['Load %'] != 'N/A') ? json['Load %'] : 0.0,
    );
  }
}
