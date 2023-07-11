class RunTime {
  final double magnitude;
  final String unit;
  final String string;

  RunTime({
    required this.magnitude,
    required this.unit,
    required this.string,
  });

  factory RunTime.fromJson(Map<String, dynamic> json) {
    return RunTime(
      magnitude: json['magnitude'].toDouble(),
      unit: json['unit'],
      string: json['string'],
    );
  }
}
