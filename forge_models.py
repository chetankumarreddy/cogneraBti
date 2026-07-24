from pathlib import Path
Path('model_vault').mkdir(exist_ok=True)
(Path('model_vault')/'model_card.json').write_text('{"model":"IsolationForest-demo","status":"ready"}')
print('Model vault ready')
