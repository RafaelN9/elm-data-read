import 'dart:convert';

import 'package:flutter/material.dart';
import 'fetchData.dart';

void main() {
  runApp(MainApp());
}

class MainApp extends StatefulWidget {
  @override
  _MainAppState createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  Stream<String>? dataStream;
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
    return MaterialApp(
        home: Scaffold(
      appBar: AppBar(
        title: const Text('StreamBuilder with RefreshIndicator'),
      ),
      body: RefreshIndicator(
        key: _refreshIndicatorKey,
        onRefresh: refreshData,
        child: (dataStream != null)
            ? StreamBuilder<String>(
                stream: dataStream,
                builder:
                    (BuildContext context, AsyncSnapshot<String> snapshot) {
                  if (snapshot.hasData) {
                    final json = jsonDecode(snapshot.data!);
                    final data = Data.fromJson(json);
                    print(data.items[0].pidName);
                    return Center(
                      child: Text(
                          '${data.items[0].pidName}: ${data.items[0].magnitude} ${data.items[0].unit}'),
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
              )
            : const Center(child: Text('No data')),
      ),
    ));
  }
}
