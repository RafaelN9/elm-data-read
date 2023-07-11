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
      dataStream =
          fetchDataFromApi(); // Replace with your own stream or data source
    });
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
                child: StreamBuilder<CarData>(
                  stream: dataStream,
                  builder:
                      (BuildContext context, AsyncSnapshot<CarData> snapshot) {
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
                                label: 'Throttle'),
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
                            // Display the fuel efficiency as a large bar
                            LargeBar(
                                percentage: data.fuelEfficiency,
                                label: 'Fuel Efficiency'),
                            // Display the runtime converting the magnitude as time duration
                            Text(
                              'Engine Runtime: ${Duration(seconds: data.runTime.magnitude.toInt()).toString().split('.').first}',
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
              ),
            )
          : const Center(child: CircularProgressIndicator()),
    );
  }
}
