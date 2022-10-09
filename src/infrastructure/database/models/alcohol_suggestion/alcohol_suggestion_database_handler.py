from bson import ObjectId
from pymongo.collection import Collection

from src.domain.alcohol_suggestion.alcohol_suggestion_create import AlcoholSuggestionCreate
from src.infrastructure.database.models.alcohol_suggestion.alcohol_suggestion import AlcoholSuggestion


class AlcoholSuggestionDatabaseHandler:

    @staticmethod
    async def get_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
            limit: int,
            offset: int,
    ) -> list[dict]:
        return list(suggestions_collection.find({}).skip(offset).limit(limit))

    @staticmethod
    async def delete_suggestion(collection: Collection[AlcoholSuggestion], suggestion_id: ObjectId) -> None:
        collection.delete_one({'_id': suggestion_id})

    @staticmethod
    async def count_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
            phrase: str
    ) -> int:
        if phrase:
            return suggestions_collection.count_documents(
                filter={'$or': [{'name': {'$regex': phrase, '$options': 'i'}},
                                {'kind': {'$regex': phrase, '$options': 'i'}}]})
        else:
            return suggestions_collection.estimated_document_count()

    @staticmethod
    async def get_suggestion_by_id(
            collection: Collection[AlcoholSuggestion],
            suggestion_id: ObjectId
    ) -> dict | None:
        return collection.find_one({'_id': suggestion_id})

    @staticmethod
    async def get_suggestion_by_barcode(
            collection: Collection[AlcoholSuggestion],
            barcode: str
    ) -> dict | None:
        return collection.find_one({'barcode': barcode})

    @staticmethod
    async def append_to_suggestion(
            collection: Collection[AlcoholSuggestion],
            user_id: ObjectId,
            description: str | None,
            suggestion: AlcoholSuggestion
    ) -> None:
        if suggestion['descriptions']:
            if description is not None:
                collection.update_one({'_id': suggestion['_id']},
                                      {'$push': {'user_ids': user_id, 'descriptions': description}})
            else:
                collection.update_one({'_id': suggestion['_id']},
                                      {'$push': {'user_ids': user_id, 'descriptions': [description]}})
        else:
            collection.update_one({'_id': suggestion['_id']}, {'$push': {'user_ids': user_id}})

    @staticmethod
    async def create_suggestion(
            collection: Collection[AlcoholSuggestion],
            user_id: ObjectId,
            payload: AlcoholSuggestionCreate
    ) -> None:
        if payload.description:
            descriptions = [payload.description]
        else:
            descriptions = None
        db_suggestions = AlcoholSuggestion(
            **payload.dict(),
            descriptions=descriptions,
            user_ids=[user_id]
        )
        collection.insert_one(db_suggestions)

    @staticmethod
    async def search_suggestions_by_phrase(
            suggestions_collection: Collection[AlcoholSuggestion],
            limit: int, offset: int,
            phrase: str
    ) -> list[dict]:
        if phrase:
            return list(suggestions_collection.find(
                {'$or': [{'name': {'$regex': phrase, '$options': 'i'}},
                         {'kind': {'$regex': phrase, '$options': 'i'}}]}).skip(
                offset).limit(limit))
        else:
            return list(suggestions_collection.find({}).skip(offset).limit(limit))
