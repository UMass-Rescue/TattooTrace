//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.12

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class TattoosRecognitionConfig {
  /// Returns a new [TattoosRecognitionConfig] instance.
  TattoosRecognitionConfig({
    this.assetId,
    required this.enabled,
    required this.minScore,
    this.mode,
    required this.modelName,
    this.modelType,
  });

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  String? assetId;

  bool enabled;

  double minScore;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  MediaMode? mode;

  String modelName;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  ModelType? modelType;

  @override
  bool operator ==(Object other) => identical(this, other) || other is TattoosRecognitionConfig &&
    other.assetId == assetId &&
    other.enabled == enabled &&
    other.minScore == minScore &&
    other.mode == mode &&
    other.modelName == modelName &&
    other.modelType == modelType;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (assetId == null ? 0 : assetId!.hashCode) +
    (enabled.hashCode) +
    (minScore.hashCode) +
    (mode == null ? 0 : mode!.hashCode) +
    (modelName.hashCode) +
    (modelType == null ? 0 : modelType!.hashCode);

  @override
  String toString() => 'TattoosRecognitionConfig[assetId=$assetId, enabled=$enabled, minScore=$minScore, mode=$mode, modelName=$modelName, modelType=$modelType]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
    if (this.assetId != null) {
      json[r'assetId'] = this.assetId;
    } else {
    //  json[r'assetId'] = null;
    }
      json[r'enabled'] = this.enabled;
      json[r'minScore'] = this.minScore;
    if (this.mode != null) {
      json[r'mode'] = this.mode;
    } else {
    //  json[r'mode'] = null;
    }
      json[r'modelName'] = this.modelName;
    if (this.modelType != null) {
      json[r'modelType'] = this.modelType;
    } else {
    //  json[r'modelType'] = null;
    }
    return json;
  }

  /// Returns a new [TattoosRecognitionConfig] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static TattoosRecognitionConfig? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      return TattoosRecognitionConfig(
        assetId: mapValueOfType<String>(json, r'assetId'),
        enabled: mapValueOfType<bool>(json, r'enabled')!,
        minScore: mapValueOfType<double>(json, r'minScore')!,
        mode: MediaMode.fromJson(json[r'mode']),
        modelName: mapValueOfType<String>(json, r'modelName')!,
        modelType: ModelType.fromJson(json[r'modelType']),
      );
    }
    return null;
  }

  static List<TattoosRecognitionConfig> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <TattoosRecognitionConfig>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = TattoosRecognitionConfig.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, TattoosRecognitionConfig> mapFromJson(dynamic json) {
    final map = <String, TattoosRecognitionConfig>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = TattoosRecognitionConfig.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of TattoosRecognitionConfig-objects as value to a dart map
  static Map<String, List<TattoosRecognitionConfig>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<TattoosRecognitionConfig>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = TattoosRecognitionConfig.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'enabled',
    'minScore',
    'modelName',
  };
}

