class AirIntake {
  final double magnitude;
  final String unit;
  final String string;

  AirIntake({
    required this.magnitude,
    required this.unit,
    required this.string,
  });

  factory AirIntake.fromJson(Map<String, dynamic> json) {
    return AirIntake(
      magnitude: json['magnitude'].toDouble(),
      unit: json['unit'],
      string: json['string'],
    );
  }
}
