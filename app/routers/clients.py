"""Client intelligence endpoints"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from app.services.intelligence_service import IntelligenceService
from app.services.ai_service import AIService
from app.utils.data_loader import DataLoader
from app.models.schemas import MeetingBrief

router = APIRouter(prefix="/clients", tags=["clients"])


def get_intelligence_service() -> IntelligenceService:
    """Dependency: Get intelligence service instance"""
    try:
        from app.config import get_settings
        settings = get_settings()
        data_loader = DataLoader(base_path=settings.data_path)
        ai_service = AIService()
        return IntelligenceService(data_loader, ai_service)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize services: {str(e)}")


@router.get("/list")
async def list_clients(service: IntelligenceService = Depends(get_intelligence_service)) -> List[Dict[str, Any]]:
    """List all available clients"""
    from app.config import get_settings
    settings = get_settings()

    sf_data = service.data_loader.load_salesforce_data()
    accounts = sf_data["accounts"]

    if accounts.empty:
        return []

    result = accounts[["AccountId", "AccountName", "Industry", "Region", "ESGDisclosureStatus"]].to_dict(orient="records")
    for client in result:
        client["logo_url"] = f"{settings.logo_base_url}/{client['AccountId']}.png"
    return result


@router.get("/{client_name}")
async def get_client(
    client_name: str,
    service: IntelligenceService = Depends(get_intelligence_service)
) -> Dict[str, Any]:
    """Get detailed client information"""
    from app.config import get_settings
    settings = get_settings()

    client_data = service.get_client_info(client_name)

    if not client_data:
        raise HTTPException(status_code=404, detail=f"Client '{client_name}' not found")

    if client_data.get("account"):
        account_id = client_data["account"].get("AccountId")
        if account_id:
            client_data["account"]["logo_url"] = f"{settings.logo_base_url}/{account_id}.png"

    return client_data


@router.post("/{client_name}/meeting-brief")
async def generate_meeting_brief(
    client_name: str,
    service: IntelligenceService = Depends(get_intelligence_service)
) -> MeetingBrief:
    """Generate comprehensive meeting preparation brief"""
    try:
        brief = service.generate_meeting_brief(client_name)
        return brief
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating brief: {str(e)}")


@router.get("/{client_name}/communications")
async def search_communications(
    client_name: str,
    query: str = None,
    service: IntelligenceService = Depends(get_intelligence_service)
) -> Dict[str, Any]:
    """Search emails and Teams chats for a client"""
    try:
        results = service.search_communications(client_name, query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching communications: {str(e)}")


@router.get("/{client_name}/action-items")
async def get_action_items(
    client_name: str,
    service: IntelligenceService = Depends(get_intelligence_service)
) -> List[Dict[str, Any]]:
    """Get action items for a client"""
    try:
        action_items = service.extract_action_items(client_name)
        return action_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting action items: {str(e)}")
