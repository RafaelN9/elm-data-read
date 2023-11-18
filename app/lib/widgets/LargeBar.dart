import 'dart:ffi';

import 'package:flutter/material.dart';

class LargeBar extends StatelessWidget {
  LargeBar({super.key, required this.percentage, required this.label});

  double percentage;
  final String label;

  @override
  Widget build(BuildContext context) {
    final cs = Theme.of(context).colorScheme;
    final porcentagemCor = percentage.toInt();

    final larguraBarra = 300 * porcentagemCor / 100;
    final alpha = (porcentagemCor > 50)
        ? ((50 - porcentagemCor) * 5.1).toInt()
        : (porcentagemCor * 5.1).toInt();
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
          height: 100,
          width: 300,
          decoration: BoxDecoration(
            color: cs.onPrimaryContainer,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Stack(
            clipBehavior: Clip.hardEdge,
            children: [
              // Display the percentage as a bar
              Container(
                height: 100,
                width: (larguraBarra < 10) ? 10 : larguraBarra,
                decoration: BoxDecoration(
                  color: (percentage > 50)
                      ? Color.fromARGB(255, alpha, 230, alpha)
                      : Color.fromARGB(255, 250, alpha, alpha),
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              // Display the percentage as text
              Center(
                child: Text(
                  '${percentage.toStringAsFixed(2)}%',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: cs.onPrimary,
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
