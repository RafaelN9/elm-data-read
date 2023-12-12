class MAF {
  final double magnitude;
  final String unit;
  final String string;

  MAF({
    required this.magnitude,
    required this.unit,
    required this.string,
  });

  factory MAF.fromJson(Map<String, dynamic> json) {
    return MAF(
      magnitude: json['magnitude'] * 1000,
      unit: 'g/s',
      string: json['string'],
    );
  }
}
