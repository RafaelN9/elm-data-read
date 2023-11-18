import 'package:flutter/material.dart';

class HalfPieChartPainter extends CustomPainter {
  // Create a custom painter to draw a half pie chart that is aligned horizontally and the arc upwards
  final double percentage;
  final ColorScheme cs;

  HalfPieChartPainter({
    required this.percentage,
    required this.cs,
  });

  @override
  void paint(Canvas canvas, Size size) {
    // Draw the background
    Paint paint = Paint()
      ..color = cs.onPrimaryContainer
      ..strokeCap = StrokeCap.round
      ..style = PaintingStyle.stroke
      ..strokeWidth = 10;
    canvas.drawArc(
      Rect.fromCenter(
        center: Offset(size.width / 2, size.height / 2),
        height: size.height,
        width: size.width,
      ),
      3.14,
      0,
      false,
      paint,
    );

    // Draw the foreground
    paint = Paint()
      ..color = cs.primary
      ..strokeCap = StrokeCap.round
      ..style = PaintingStyle.stroke
      ..strokeWidth = 10;
    canvas.drawArc(
      Rect.fromCenter(
        center: Offset(size.width / 2, size.height / 2),
        height: size.height,
        width: size.width,
      ),
      3.14,
      percentage * 3.14,
      false,
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}

class HalfPieChart extends StatelessWidget {
  HalfPieChart(
      {required this.percentage, required this.innerText, this.label = ''});

  final double percentage;
  final String label;
  final String innerText;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        (label != '')
            ? Text(
                label,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                ),
              )
            : Container(),
        Container(
          margin: const EdgeInsets.all(16),
          height: 100,
          width: 100,
          child: Stack(
            children: [
              // Display the percentage as a half pie chart
              Container(
                height: 100,
                width: 100,
                child: CustomPaint(
                  painter: HalfPieChartPainter(
                    cs: Theme.of(context).colorScheme,
                    percentage: percentage,
                  ),
                ),
              ),
              // Display the percentage as text
              Center(
                child: Text(
                  innerText,
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
