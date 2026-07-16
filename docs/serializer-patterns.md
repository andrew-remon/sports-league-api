# Serializer Patterns

## 1. Read/Write Asymmetry

Read Nested Fields during serialization → GET
Write Fields to include in representation → POST

```python
    class PlayerSerializer(serializers.ModelSerializer):
        team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation["team"] = TeamDetailSerializer(instance.team, context=self.context).data
            return representation
```

Use: When GET consumers need rich nested data but POST consumers should only send an ID.
Don't Use: When read and write shapes are identical — asymmetry adds complexity for no gain.

## 2. Writable Nested Create
```python
    def create(self, validated_data):
        match = None
        result_data = validated_data.pop('result', None)
        if result_data is not None:
            with transaction.atomic():
                validated_data['status'] = Match.MatchStatus.COMPLETED
                match = Match.objects.create(**validated_data)
                MatchResult.objects.create(match=match, **result_data)
        else:
            validated_data['status'] = Match.MatchStatus.SCHEDULED
            match = Match.objects.create(**validated_data)

        return match
```

Use: When there are related models (Match + MatchSerializer) that are needed to be handled using SerializerField
Don't Use: When you only need to reference an existing related object by ID — use PrimaryKeyRelatedField instead. Writable nested is for creating new related objects, not linking to existing ones."

## 3. Computed Fields

### SerializerMethodField
- When to use: When we need to access the method on the request/context and for API
- When NOT to use: When we need to use it outside the context layer (in admin, shell, ORM)

- Sports League API example:
```python
    full_name = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
```

### @property
- When to use: When we need to access the method everywhere (shell, admin, management commands, ORM)
- When NOT to use: when the method needs to be exposed on the API (request) layer.

- Sports League API example:
```python
    @property
    def winner(self) -> "Team | None":
        if self.status != Match.MatchStatus.COMPLETED:
            return None

        if self.result.home_score > self.result.away_score:
            return self.home_team
        elif self.result.home_score < self.result.away_score:
            return self.away_team
        else:
            return None
```
