enum TaskStatus {
  todo,
  doing,
  done;

  static TaskStatus fromJson(String value) => switch (value) {
        'todo' => TaskStatus.todo,
        'doing' => TaskStatus.doing,
        'done' => TaskStatus.done,
        _ => throw FormatException('Trạng thái không hợp lệ: $value'),
      };
}

/// Ví dụ model bất biến đã hoàn thành để học cách đọc và kiểm thử code.
///
/// `DateTime` được chuẩn hóa về UTC. Các quy tắc phía client không thay thế
/// validation và authorization ở backend.
class WorkTask {
  factory WorkTask({
    required String id,
    required String title,
    String description = '',
    TaskStatus status = TaskStatus.todo,
    DateTime? dueAt,
    required DateTime updatedAt,
    int version = 1,
    required String ownerId,
  }) {
    final cleanTitle = title.trim();
    if (cleanTitle.isEmpty || cleanTitle.length > 120) {
      throw ArgumentError.value(title, 'title', 'Cần 1–120 ký tự sau trim');
    }
    if (id.trim().isEmpty || ownerId.trim().isEmpty) {
      throw ArgumentError('id và ownerId không được rỗng');
    }
    if (version < 1) {
      throw ArgumentError.value(version, 'version', 'Phải >= 1');
    }
    return WorkTask._(
      id: id,
      title: cleanTitle,
      description: description,
      status: status,
      dueAt: dueAt?.toUtc(),
      updatedAt: updatedAt.toUtc(),
      version: version,
      ownerId: ownerId,
    );
  }

  const WorkTask._({
    required this.id,
    required this.title,
    required this.description,
    required this.status,
    required this.dueAt,
    required this.updatedAt,
    required this.version,
    required this.ownerId,
  });

  factory WorkTask.fromJson(Map<String, Object?> json) {
    final dueAt = json['dueAt'];
    return WorkTask(
      id: json['id'] as String,
      title: json['title'] as String,
      description: json['description'] as String? ?? '',
      status: TaskStatus.fromJson(json['status'] as String),
      dueAt: dueAt == null ? null : DateTime.parse(dueAt as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
      version: json['version'] as int,
      ownerId: json['ownerId'] as String,
    );
  }

  final String id;
  final String title;
  final String description;
  final TaskStatus status;
  final DateTime? dueAt;
  final DateTime updatedAt;
  final int version;
  final String ownerId;

  /// clearDueAt phân biệt "không đổi hạn" và "xóa hạn".
  ///
  /// Đây là một lựa chọn đơn giản cho bài học; có thể thay bằng sentinel hoặc
  /// kiểu biểu diễn thay đổi rõ ràng khi xây API cập nhật phức tạp hơn.
  WorkTask copyWith({
    String? title,
    String? description,
    TaskStatus? status,
    DateTime? dueAt,
    bool clearDueAt = false,
    DateTime? updatedAt,
    int? version,
  }) =>
      WorkTask(
        id: id,
        title: title ?? this.title,
        description: description ?? this.description,
        status: status ?? this.status,
        dueAt: clearDueAt ? null : dueAt ?? this.dueAt,
        updatedAt: updatedAt ?? this.updatedAt,
        version: version ?? this.version,
        ownerId: ownerId,
      );

  Map<String, Object?> toJson() => {
        'id': id,
        'title': title,
        'description': description,
        'status': status.name,
        'dueAt': dueAt?.toIso8601String(),
        'updatedAt': updatedAt.toIso8601String(),
        'version': version,
        'ownerId': ownerId,
      };
}
