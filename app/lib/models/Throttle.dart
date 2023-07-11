class Throttle {
  final double magnitude;
  final String unit;
  final String string;

  Throttle({
    required this.magnitude,
    required this.unit,
    required this.string,
  });

  factory Throttle.fromJson(Map<String, dynamic> json) {
    return Throttle(
      magnitude: json['magnitude'].toDouble(),
      unit: json['unit'],
      string: json['string'],
    );
  }
}
