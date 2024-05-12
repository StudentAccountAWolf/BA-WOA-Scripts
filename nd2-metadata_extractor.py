import nd2
import os
from ome_types import to_dict

# Ordnerpfad
folder_path = input(r"Folder directory:")
count = 0

# Durchlaufe alle Dateien im Ordner
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        # Überprüfe, ob die Datei eine ND2-Datei ist
        if file_name.endswith(".nd2"):
            # Vollständigen Pfad zur ND2-Datei erstellen
            file_path = os.path.join(root, file_name)
            
            # ND2-Datei öffnen
            with nd2.ND2File(file_path) as ndfile:
                # Metadaten extrahieren
                attributes = ndfile.attributes
                metadata = ndfile.metadata
                voxel_size = ndfile.voxel_size()
                experiment = ndfile.experiment
                text_info = ndfile.text_info
                rois = ndfile.rois
                binary_data = ndfile.binary_data
                events = ndfile.events()
                ome_metadata = ndfile.ome_metadata()
                unstructured_metadata = ndfile.unstructured_metadata()

                # Ausgabedatei für Metadaten erstellen
                output_file_path = os.path.splitext(file_path)[0] + "-Metadata.txt"

                # Metadaten in die Datei schreiben
                with open(output_file_path, 'w') as f:
                    # Schreibe Attributinformationen
                    if attributes is not None:
                        attribute_info = {
                            "bitsPerComponentInMemory": "int",
                            "bitsPerComponentSignificant": "int",
                            "channelCount": "int | None = None",
                            "componentCount": "int",
                            "compressionLevel": "float | None = None",
                            "compressionType": "Literal['lossless', 'lossy', 'none'] | None = None",
                            "heightPx": "int",
                            "pixelDataType": "Literal['float', 'unsigned']",
                            "sequenceCount": "int",
                            "tileHeightPx": "int | None = None",
                            "tileWidthPx": "int | None = None",
                            "widthBytes": "int | None = None",
                            "widthPx": "int | None = None"
                        }
                        f.write("------Attributes------\n")
                        for attr_name, attr_type in attribute_info.items():
                                attr_value = getattr(attributes, attr_name, None)
                                if attr_value is not None:
                                    f.write(f"{attr_name}: {attr_value}\n")

                    # Schreibe allgemeine Metadaten
                    if metadata is not None:
                        f.write("\n------General Metadata------\n")
                        for channel in metadata.channels:
                            channel_meta = channel.channel
                            volume = channel.volume
                            f.write(f"Channel: {channel_meta.index}\n")
                            f.write(f"Name: {channel_meta.name}\n")
                            f.write(f"Color: ({channel_meta.color.r},{channel_meta.color.g},{channel_meta.color.b},{channel_meta.color.a})\n")
                            f.write(f"EmissionLambdaNm: {channel_meta.emissionLambdaNm}\n")
                            f.write(f"ExcitationLambdaNm: {channel_meta.excitationLambdaNm}\n")
                            f.write(f"ObjectiveMagnification: {channel.microscope.objectiveMagnification}\n")
                            f.write(f"ObjectiveName: {channel.microscope.objectiveName}\n")
                            f.write(f"ObjectiveNumericalAperture: {channel.microscope.objectiveNumericalAperture}\n")
                            f.write(f"ZoomMagnification: {channel.microscope.zoomMagnification}\n")
                            f.write(f"ImmersionRefractiveIndex: {channel.microscope.immersionRefractiveIndex}\n")
                            f.write(f"ProjectiveMagnification: {channel.microscope.projectiveMagnification}\n")
                            f.write(f"PinholeDiameterUm: {channel.microscope.pinholeDiameterUm}\n")
                            f.write(f"ModalityFlags: {channel.microscope.modalityFlags}\n")
                            f.write(f"AxesCalibrated: {volume.axesCalibrated}\n")
                            f.write(f"AxesCalibration: {volume.axesCalibration}\n")
                            f.write(f"AxesInterpretation: {volume.axesInterpretation}\n")
                            f.write(f"BitsPerComponentInMemory: {volume.bitsPerComponentInMemory}\n")
                            f.write(f"BitsPerComponentSignificant: {volume.bitsPerComponentSignificant}\n")
                            f.write(f"CameraTransformationMatrix: {volume.cameraTransformationMatrix}\n")
                            f.write(f"ComponentCount: {volume.componentCount}\n")
                            f.write(f"ComponentDataType: {volume.componentDataType}\n")
                            f.write(f"VoxelCount: {volume.voxelCount}\n")
                            f.write(f"ComponentMaxima: {volume.componentMaxima}\n")
                            f.write(f"ComponentMinima: {volume.componentMinima}\n")
                            f.write(f"PixelToStageTransformationMatrix: {volume.pixelToStageTransformationMatrix}\n")

                    # Schreibe Informationen über die Voxelgröße
                    
                    if voxel_size is not None:
                        f.write("\n------Voxel Size------\n")
                        f.write(f"X: {voxel_size.x}\n")
                        f.write(f"Y: {voxel_size.y}\n")
                        f.write(f"Z: {voxel_size.z}\n")

                    # Schreibe Informationen über Experimente
                    
                    if experiment is not None:
                        f.write("\n------Experiments------\n")
                        for exp in experiment:
                            f.write(f"{exp}\n")

                    # Schreibe Textinformationen
                    
                    if text_info is not None:
                        f.write("\n------Text Information------\n")
                        for key, value in text_info.items():
                            f.write(f"{key}: {value}\n")

                    # Schreibe Informationen über ROIs
                    
                    if rois is not None:
                        f.write("\n------ROIs------\n")
                        for roi_id, roi in rois.items():
                            f.write(f"ROI {roi_id}\n")
                            for roi_attr, roi_val in roi.__dict__.items():
                                f.write(f"{roi_attr}: {roi_val}\n")

                    # Schreibe Informationen über binäre Daten
                    
                    if binary_data is not None:
                        f.write("\n------Binary Data------\n")
                        for binary_layer in binary_data:
                            f.write(f"Binary Layer: {binary_layer.name}\n")
                            for frame_idx, frame_data in enumerate(binary_layer.data):
                                if frame_data is not None:
                                    f.write(f"Frame {frame_idx}\n")
                                    f.write(f"{frame_data}\n")

                    # Schreibe Informationen über Events
                    
                    if events is not None:
                        f.write("\n------Events------\n")
                        for event in events:
                            for key, value in event.items():
                                f.write(f"{key}: {value}\n")
                            f.write("\n")

                    # Schreibe Informationen über OME-Metadaten
                    
                    if ome_metadata is not None:
                        f.write("\n------OME-Metadata------\n")
                        ome_dict = to_dict(ome_metadata)
                        structured_annotations = ome_dict.get("structured_annotations", {}).get("map_annotations", [])
                        for annotation in structured_annotations:
                            f.write(f"Annotation: {annotation['id']}")
                            annotation_values = annotation['value']
                            for key, value in annotation_values.items():
                                f.write(f"{key}: {value}")

                    # Schreibe unstrukturierte Metadaten
                    
                    if unstructured_metadata is not None:
                        f.write("\n------Unstructured Metadata------\n")
                        f.write(f"{unstructured_metadata}")

                    print(f"Metadata für {file_name} in {output_file_path} geschrieben")
                    count += 1

print(f"Gesamtanzahl verarbeiteter Dateien: {count}")
exit
