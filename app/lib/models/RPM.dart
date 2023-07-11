class RPM {
  final double magnitude;
  final String unit;
  final String string;

  RPM({
    required this.magnitude,
    required this.unit,
    required this.string,
  });

  factory RPM.fromJson(Map<String, dynamic> json) {
    return RPM(
      magnitude: json['magnitude'].toDouble(),
      unit: json['unit'],
      string: json['string'],
    );
  }
}
