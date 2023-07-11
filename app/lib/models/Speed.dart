class Speed {
  final double magnitude;
  final String unit;
  final String string;

  Speed({
    required this.magnitude,
    required this.unit,
    required this.string,
  });

  factory Speed.fromJson(Map<String, dynamic> json) {
    return Speed(
      magnitude: json['magnitude'].toDouble(),
      unit: json['unit'],
      string: json['string'],
    );
  }
}
