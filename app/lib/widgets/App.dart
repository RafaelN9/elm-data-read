import 'dart:io';

import 'package:flutter/material.dart';

import 'package:app/models/CarData.dart';
import 'package:app/widgets/HalfPieChart.dart';
import 'package:app/widgets/LargeBar.dart';
import 'package:app/widgets/SmallBar.dart';
import '../fetch_data.dart';

class App extends StatefulWidget {
  const App({Key? key, Stream<CarData>? dataStream}) : super(key: key);
  @override
  _AppState createState() => _AppState();
}

class _AppState extends State<App> {
  String tipoCombustivel = "gasoline";
  Stream<CarData>? dataStream;
  final GlobalKey<RefreshIndicatorState> _refreshIndicatorKey =
      GlobalKey<RefreshIndicatorState>();

  @override
  void initState() {
    super.initState();
    dataStream =
        fetchDataFromApi(); // Replace with your own stream or data source
  }

  Future<void> refreshData() async {
    // Refresh your data source here, for example, fetching new data from an API
    setState(() {
      while (dataStream == null) {
        sleep(const Duration(seconds: 3));
        dataStream =
            fetchDataFromApi(); // Replace with your own stream or data source
      }
    });
  }

  double calculateFuelRate(double maf, double afr, String fuelType) {
    // Calculate fuel consumption rate in g/s
    double fuelConsumptionRate = maf / afr;
    // Return the fuel consumption rate in L/s
    return fuelConsumptionRate > 0.000001 ? fuelConsumptionRate : 0.000001;
  }

  calculateFuelEfficiency(double maf, double speed) {
    double fuelConsumptionLs = calculateFuelRate(
      maf,
      tipoCombustivel == "gasoline" ? 14.7 : 9.0,
      tipoCombustivel,
    );

    double fuelEfficiency = speed * 1090 / fuelConsumptionLs;

    if (tipoCombustivel == "gasoline") {
      const max_gas = 4742808.0;
      const min_gas = 148212.75;
      return (fuelEfficiency - min_gas) / (max_gas - min_gas);
    } else {
      const max_eth = 3096036.0;
      const min_eth = 86001.0;
      return (fuelEfficiency - min_eth) / (max_eth - min_eth);
    }
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      key: _refreshIndicatorKey,
      onRefresh: refreshData,
      child: (dataStream != null)
          ? SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              child: SizedBox(
                // take all available height
                height: MediaQuery.of(context).size.height - 100,
                child: Column(
                  children: [
                    Switch(
                        value: tipoCombustivel == "gasoline",
                        onChanged: (value) {
                          setState(() {
                            tipoCombustivel = value ? "gasoline" : "ethanol";
                          });
                        }),
                    StreamBuilder<CarData>(
                      stream: dataStream,
                      builder: (BuildContext context,
                          AsyncSnapshot<CarData> snapshot) {
                        if (snapshot.hasData) {
                          var data = snapshot.data!.data;
                          return Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                // Display the throttle as a small bar
                                SmallBar(
                                    percentage: data.throttle.magnitude,
                                    innerText:
                                        '${data.throttle.magnitude.toStringAsFixed(0)}%',
                                    label: 'Acelerador'),
                                // Display the speed as a half pie chart
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    HalfPieChart(
                                      percentage: data.speed.magnitude / 200,
                                      innerText:
                                          '${data.speed.magnitude.toStringAsFixed(0)} \nkm/h',
                                    ),
                                    HalfPieChart(
                                      percentage: data.rpm.magnitude / 8000,
                                      innerText:
                                          '${data.rpm.magnitude.toStringAsFixed(0)} \nRPM',
                                    ),
                                  ],
                                ),
                                LargeBar(
                                    percentage: calculateFuelEfficiency(
                                      data.maf.magnitude,
                                      data.speed.magnitude,
                                    ),
                                    label: 'Eficiência de combustível'),
                                Text(
                                  'Tempo: ${Duration(seconds: data.runTime.magnitude.toInt()).toString().split('.').first}',
                                  style: const TextStyle(
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          );
                        } else if (snapshot.hasError) {
                          return Center(
                            child: Text('Error: ${snapshot.error}'),
                          );
                        } else {
                          return const Center(
                            child: CircularProgressIndicator(),
                          );
                        }
                      },
                    ),
                  ],
                ),
              ),
            )
          : const Center(child: CircularProgressIndicator()),
    );
  }
}
