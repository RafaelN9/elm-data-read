import 'package:flutter/material.dart';

class SmallBar extends StatelessWidget {
  SmallBar(
      {required this.percentage, required this.innerText, required this.label});

  final double percentage;
  final String label;
  final String innerText;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        Container(
          margin: const EdgeInsets.all(16),
          height: 20,
          width: 300,
          decoration: BoxDecoration(
            color: Colors.grey[300],
            borderRadius: BorderRadius.circular(8),
          ),
          child: Stack(
            children: [
              // Display the percentage as a bar
              Container(
                height: 20,
                width: 300 * percentage / 100,
                decoration: BoxDecoration(
                  color: Colors.green,
                  borderRadius: BorderRadius.circular(8),
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
