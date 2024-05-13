//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.12

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class TattoosRecognitionResponseDto {
  /// Returns a new [TattoosRecognitionResponseDto] instance.
  TattoosRecognitionResponseDto({
    required this.filePath,
    required this.id,
    required this.mediaMode,
  });

  /// Path to the media file
  String filePath;

  String id;

  /// Media type (image|video)
  TattoosRecognitionResponseDtoMediaModeEnum mediaMode;

  @override
  bool operator ==(Object other) => identical(this, other) || other is TattoosRecognitionResponseDto &&
    other.filePath == filePath &&
    other.id == id &&
    other.mediaMode == mediaMode;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (filePath.hashCode) +
    (id.hashCode) +
    (mediaMode.hashCode);

  @override
  String toString() => 'TattoosRecognitionResponseDto[filePath=$filePath, id=$id, mediaMode=$mediaMode]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
      json[r'filePath'] = this.filePath;
      json[r'id'] = this.id;
      json[r'mediaMode'] = this.mediaMode;
    return json;
  }

  /// Returns a new [TattoosRecognitionResponseDto] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static TattoosRecognitionResponseDto? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      return TattoosRecognitionResponseDto(
        filePath: mapValueOfType<String>(json, r'filePath')!,
        id: mapValueOfType<String>(json, r'id')!,
        mediaMode: TattoosRecognitionResponseDtoMediaModeEnum.fromJson(json[r'mediaMode'])!,
      );
    }
    return null;
  }

  static List<TattoosRecognitionResponseDto> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <TattoosRecognitionResponseDto>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = TattoosRecognitionResponseDto.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, TattoosRecognitionResponseDto> mapFromJson(dynamic json) {
    final map = <String, TattoosRecognitionResponseDto>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = TattoosRecognitionResponseDto.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of TattoosRecognitionResponseDto-objects as value to a dart map
  static Map<String, List<TattoosRecognitionResponseDto>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<TattoosRecognitionResponseDto>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = TattoosRecognitionResponseDto.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'filePath',
    'id',
    'mediaMode',
  };
}

/// Media type (image|video)
class TattoosRecognitionResponseDtoMediaModeEnum {
  /// Instantiate a new enum with the provided [value].
  const TattoosRecognitionResponseDtoMediaModeEnum._(this.value);

  /// The underlying value of this enum member.
  final String value;

  @override
  String toString() => value;

  String toJson() => value;

  static const image = TattoosRecognitionResponseDtoMediaModeEnum._(r'image');
  static const video = TattoosRecognitionResponseDtoMediaModeEnum._(r'video');

  /// List of all possible values in this [enum][TattoosRecognitionResponseDtoMediaModeEnum].
  static const values = <TattoosRecognitionResponseDtoMediaModeEnum>[
    image,
    video,
  ];

  static TattoosRecognitionResponseDtoMediaModeEnum? fromJson(dynamic value) => TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer().decode(value);

  static List<TattoosRecognitionResponseDtoMediaModeEnum> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <TattoosRecognitionResponseDtoMediaModeEnum>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = TattoosRecognitionResponseDtoMediaModeEnum.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }
}

/// Transformation class that can [encode] an instance of [TattoosRecognitionResponseDtoMediaModeEnum] to String,
/// and [decode] dynamic data back to [TattoosRecognitionResponseDtoMediaModeEnum].
class TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer {
  factory TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer() => _instance ??= const TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer._();

  const TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer._();

  String encode(TattoosRecognitionResponseDtoMediaModeEnum data) => data.value;

  /// Decodes a [dynamic value][data] to a TattoosRecognitionResponseDtoMediaModeEnum.
  ///
  /// If [allowNull] is true and the [dynamic value][data] cannot be decoded successfully,
  /// then null is returned. However, if [allowNull] is false and the [dynamic value][data]
  /// cannot be decoded successfully, then an [UnimplementedError] is thrown.
  ///
  /// The [allowNull] is very handy when an API changes and a new enum value is added or removed,
  /// and users are still using an old app with the old code.
  TattoosRecognitionResponseDtoMediaModeEnum? decode(dynamic data, {bool allowNull = true}) {
    if (data != null) {
      switch (data) {
        case r'image': return TattoosRecognitionResponseDtoMediaModeEnum.image;
        case r'video': return TattoosRecognitionResponseDtoMediaModeEnum.video;
        default:
          if (!allowNull) {
            throw ArgumentError('Unknown enum value to decode: $data');
          }
      }
    }
    return null;
  }

  /// Singleton [TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer] instance.
  static TattoosRecognitionResponseDtoMediaModeEnumTypeTransformer? _instance;
}


