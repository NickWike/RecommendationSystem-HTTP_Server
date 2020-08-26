class ProductCardBean:

    @staticmethod
    def row_to_dict(row):
        product_info = {"product_id": str(row[0]).zfill(11),
                        "product_name": row[1],
                        "product_image": row[2],
                        "price": str(row[3]),
                        "average_score": str(row[4]),
                        "comment_count": row[5]}
        return product_info
