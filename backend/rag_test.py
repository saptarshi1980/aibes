from app.rag.index_service import IndexService

service = IndexService()

service.build_index(
    bidder_id="d360ba6c-5e6b-4e62-9a30-67f5505c7e52",
    file_path=r"D:\AIBES\backend\storage\tenders\073c8883-c351-4688-82d4-92dabc87947b_DPL_PUR_ITC_06_26-27\bidders\CERF\TECHNICAL_BID_ba4a8cc0-abbd-4310-bbb6-3e935f19dfad.txt"
)