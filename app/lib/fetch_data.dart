import 'dart:async';
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'package:app/models/CarData.dart';

Stream<CarData> fetchDataFromApi() async* {
  final url =
      Uri.parse("${dotenv.env['API_URL'] ?? 'http://localhost:5000'}/stream");
  print(url);
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
      // parse json to CarData object

      if (response.isEmpty) {
        continue;
      }
      final read = CarData.fromJson(jsonDecode(response));
      yield read;
    }
  } catch (e) {
    print("Error: $e");
  } finally {
    client.close();
  }
}
