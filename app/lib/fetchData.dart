import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class DataItem {
  final String pidName;
  final String unit;
  final double magnitude;
  final String string;

  DataItem({
    required this.pidName,
    required this.unit,
    required this.magnitude,
    required this.string,
  });

  factory DataItem.fromJson(Map<String, dynamic> json) {
    return DataItem(
      pidName: json['PID name'],
      unit: json['unit'],
      magnitude: json['magnitude'].toDouble(),
      string: json['string'],
    );
  }
}

class Data {
  final List<DataItem> items;

  Data({required this.items});

  factory Data.fromJson(Map<String, dynamic> json) {
    final readObject = json['read'] as List<dynamic>;
    final items = readObject
        .map((item) => DataItem.fromJson(item as Map<String, dynamic>))
        .toList();

    return Data(items: items);
  }
}

Stream<String> fetchDataFromApi() async* {
  final url = Uri.parse('http://192.168.1.7:5000/stream');
  final client = http.Client();

  try {
    final request = http.Request('GET', url);
    final response = await client.send(request);

    // Read and print the chunks from the response stream
    await for (var chunk in response.stream.transform(utf8.decoder)) {
      //filter out content between <script> from snapshot
      var response = chunk.split('<script>')[0];
      // set all ' to "
      response = response.replaceAll("'", '"');
      yield response;
    }
  } catch (e) {
    print("Error: $e");
  } finally {
    client.close();
  }
}
