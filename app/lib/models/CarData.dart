import 'package:app/models/Data.dart';

class CarData {
  final String time;
  final Data data;

  CarData({
    required this.time,
    required this.data,
  });

  factory CarData.fromJson(Map<String, dynamic> json) {
    return CarData(
      time: json['time'],
      data: Data.fromJson(json['data']),
    );
  }
}
